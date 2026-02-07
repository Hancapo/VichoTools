from __future__ import annotations
from ..vicho_dependencies import dependencies_manager as d
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from CodeWalker.GameFiles import GameFileCache, YdrFile, YftFile, Drawable, Texture # type: ignore
    from System.Collections.Generic import HashSet # type: ignore
from pathlib import Path
from ..shared.helper import set_sollumz_import_settings
import bpy
from ..shared.funcs import create_temp_folder
import traceback



def add_entity_to_scene(name: str) -> bool:
    if bpy.context.scene.add_asset_to_scene:
        asset = bpy.data.objects.get(name)
        if not asset:
            asset = next((obj for obj in bpy.data.objects if name in obj.name), None)
        if asset and asset.asset_data:
            new_obj = asset.copy()
            new_obj.data = asset.data.copy()
            bpy.context.collection.objects.link(new_obj)
            return True
    return False
            


def process_rage_file(rage_file: "YdrFile" | "YftFile", format: str, gamecache: "GameFileCache") -> bool:
    try:
        print("Loading " + rage_file.Name)
        temp_folder: str = create_temp_folder()
        print(temp_folder)
        textures: "HashSet[Texture]" = d.HashSet[d.GameFiles.Texture]()
        texturesMissing: "HashSet[str]" = d.HashSet[str]()
        extract_path: Path = Path(temp_folder, "alltextures")
        parent_path: Path = extract_path.parent
        print(f"textures path: {str(extract_path)}")
        extract_path.mkdir(parents=True, exist_ok=True)
        drawable: "Drawable" = (
            rage_file.Drawable if format == "ydr" else rage_file.Fragment.Drawable
        )
        if drawable:
            d.Task.Run(
                d.Action(
                    lambda: d.CollectTextures(
                        drawable, textures, texturesMissing, gamecache
                    )
                )
            ).Wait()
        d.Task.Run(
            d.Action(lambda: d.WriteTexturesAsync(textures, str(extract_path)))
        ).Wait()
        rage_file_path: Path = Path(parent_path, rage_file.Name)
        d.File.WriteAllBytes(str(rage_file_path), rage_file.Save())
        import_asset_sollumz(str(rage_file_path))
        bpy.ops.file.find_missing_files(directory=str(extract_path))
        return True
    except Exception as e:
        print(e)
        return False


def get_asset_from_pm(name: str, gamecache: "GameFileCache") -> bool:
    entity_uint: int = d.JenkHash.GenHash(name)
    print(entity_uint)
    ydr: "YdrFile"
    yft: "YftFile"
    if (ydr := d.gamecache.GetYdr(entity_uint)) is not None:
        ydr.Load(ydr.RpfFileEntry.File.ExtractFile(ydr.RpfFileEntry), ydr.RpfFileEntry)
        process_rage_file(ydr, "ydr", gamecache)
        return True
    elif (yft := d.gamecache.GetYft(entity_uint)) is not None:
        yft.Load(yft.RpfFileEntry.File.ExtractFile(yft.RpfFileEntry), yft.RpfFileEntry)
        process_rage_file(yft, "yft", gamecache)
        return True
    return False

def import_asset_sollumz(p: str):
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    set_sollumz_import_settings(True)
    p_path: Path = Path(p)
    bpy.ops.sollumz.import_assets(
        directory=str(p_path.parent), files=[{"name": p_path.name}]
    )