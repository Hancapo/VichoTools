from ..vicho_dependencies import dependencies_manager as d
import tempfile
from pathlib import Path
from ..ymap.helper import set_sollumz_import_settings
import bpy

def update_status():
    return d.Action[str](lambda x: print(x))

def load_gta_cache(path: str) -> bool:
    try:
        d.GTA5Keys.LoadFromPath(path)
        d.gamecache = d.GameFileCache(
            2147483648,
            10,
            path,
            False,
            "mp2025_01_g9ec",
            False,
            "Installers;_CommonRedist",
        )
        d.gamecache.LoadAudio = False
        d.gamecache.LoadVehicles = False
        d.gamecache.LoadPeds = False
        d.gamecache.Init(update_status(), update_status())
        return True
    except Exception as e:
        print(f"Error detail: {e}")
        import traceback

        traceback.print_exc()
        return False


def create_temp_folder():
    return tempfile.mkdtemp()


def extract_asset_xml(rage_file, format: str, gamecache) -> bool:
    try:
        print("Loading " + rage_file.Name)
        temp_folder: str = create_temp_folder()
        print(temp_folder)
        filename = d.String.Empty
        xml_content, filename = d.MetaXml.GetXml(rage_file, filename, f"{str(temp_folder)}/{rage_file.Name.split('.')[0]}")
        xml_file = f"{temp_folder}/{rage_file.Name}.xml"
        d.File.WriteAllText(str(xml_file), xml_content)
        textures = d.HashSet[d.GameFiles.Texture]()
        texturesMissing = d.HashSet[str]()
        extract = Path(temp_folder, "alltextures")
        print(f"textures path: {str(extract)}")
        extract.mkdir(parents=True, exist_ok=True)
        match format:
            case "ydr":
                if rage_file.Drawable:
                    d.Task.Run(d.Action(
                        lambda: d.CollectTextures(
                            rage_file.Drawable, textures, texturesMissing, gamecache
                        ))
                    ).Wait()
            case "yft":
                pass
            case "ydd":
                pass
        d.Task.Run(d.Action(lambda: d.WriteTexturesAsync(textures, str(extract)))).Wait()
        import_asset_sollumz(xml_file)
        bpy.ops.file.find_missing_files(directory=str(extract))
        return True
    except Exception as e:
        print(e)
        return False


def import_asset_from_pm(name: str, gamecache) -> bool:
    entity_uint: int = d.JenkHash.GenHash(name)
    print(entity_uint)
    if (ydr := d.gamecache.GetYdr(entity_uint)) is not None:
        print("YDR found!")
        ydr.Load(ydr.RpfFileEntry.File.ExtractFile(ydr.RpfFileEntry), ydr.RpfFileEntry)
        extract_asset_xml(ydr, "ydr", gamecache)
        return True
    elif (yft := d.gamecache.GetYft(entity_uint)) is not None:
        pass
        #yft.Load(yft.RpfFileEntry.File.ExtractFile(yft.RpfFileEntry), yft.RpfFileEntry)
    elif (ydd := d.gamecache.GetYdd(entity_uint)) is not None:
        pass
        #ydd.Load(ydd.RpfFileEntry.File.ExtractFile(ydd.RpfFileEntry), ydd.RpfFileEntry)
    return False


def import_asset_sollumz(p: str):
    set_sollumz_import_settings(True)
    p_path = Path(p)
    bpy.ops.sollumz.import_assets(directory=str(p_path.parent), files=[{"name": p_path.stem + ".xml"}])
