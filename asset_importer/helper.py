from __future__ import annotations
import bpy
from ..vicho_dependencies import dependencies_manager as d
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from CodeWalker.GameFiles import YdrFile, YftFile # type: ignore
from pathlib import Path
from ..shared.helper import set_sollumz_import_settings
from ..shared.funcs import create_temp_folder
from .core import get_rage_file_from_pm, extract_rage_file_to_path, get_textures

def import_asset_sollumz(p: str):
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    set_sollumz_import_settings(import_as_asset=True)
    p_path: Path = Path(p)
    bpy.ops.sollumz.import_assets(
        directory=str(p_path.parent), files=[{"name": p_path.name}]
    )

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

def import_loop():
    imported_asset = get_asset_name()
    if not bpy.context.scene.is_vicho_server_running:
        return None
    if imported_asset != "":
        print("Received " + imported_asset)
        #get rage file from the game's cache
        rg_file: "YdrFile" | "YftFile" = get_rage_file_from_pm(imported_asset, d.gamecache)
        #extract file to a dir
        if rg_file:
            temp_path: str = create_temp_folder()
            #extract textures to the same path
            textures_path: str = get_textures(rg_file, d.gamecache, temp_path)
            rage_path: str = extract_rage_file_to_path(temp_path, rg_file)
            import_asset_sollumz(rage_path)
            bpy.ops.file.find_missing_files(directory=str(textures_path))
            if bpy.context.scene.add_asset_to_scene:
                add_entity_to_scene(imported_asset)
        set_asset_name("")
    return 0.1

def get_asset_name() -> str:
    return bpy.context.scene.asset_archetype_name

def set_asset_name(name: str) -> None:
    bpy.context.scene.asset_archetype_name = name

def get_category_name() -> str:
    return bpy.context.scene.asset_category_name

def set_category_name(name: str) -> None:
    bpy.context.scene.asset_category_name = name