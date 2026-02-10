from ..vicho_dependencies import dependencies_manager as d
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from CodeWalker.GameFiles import GameFileCache, YdrFile, YftFile, Texture, Drawable # type: ignore
    from System.Collections.Generic import HashSet # type: ignore
from pathlib import Path

def get_rage_file_from_pm(name: str, gamecache: "GameFileCache") -> "YftFile | YdrFile":
    entity_uint: int = d.JenkHash.GenHash(name)
    if (ydr := gamecache.GetYdr(entity_uint)) is not None:
        ydr.Load(ydr.RpfFileEntry.File.ExtractFile(ydr.RpfFileEntry), ydr.RpfFileEntry)
        return ydr
    elif (yft := gamecache.GetYft(entity_uint)) is not None:
        yft.Load(yft.RpfFileEntry.File.ExtractFile(yft.RpfFileEntry), yft.RpfFileEntry)
        return yft
    return None


def extract_rage_file_to_path(parent: str, rage_file: "YdrFile |YftFile") -> str | None:
    """Extracts a Rage file to a path and returns the path."""
    if rage_file:
        extract_path: Path = Path(parent, rage_file.Name)
        Path(parent).mkdir(parents=True, exist_ok=True)
        d.File.WriteAllBytes(str(extract_path), rage_file.Save())
        return str(extract_path)
    else:
        return None
    
def get_textures(rage_file: "YdrFile | YftFile", gamecache: "GameFileCache", path: Path) -> str:
    textures: "HashSet[Texture]" = d.HashSet[d.GameFiles.Texture]()
    texturesMissing: "HashSet[str]" = d.HashSet[str]()
    extract_path: Path = Path(path, "alltextures")
    extract_path.mkdir(parents=True, exist_ok=True)
    rage_format: str = get_rf_fmt(rage_file)
    drawable: "Drawable" = rage_file.Drawable if rage_format == "ydr" else rage_file.Fragment.Drawable
    if drawable:
        d.Task.Run(d.Action(lambda: d.CollectTextures(drawable, textures, texturesMissing, gamecache))).Wait()
        d.Task.Run(d.Action(lambda: d.WriteTexturesAsync(textures, str(extract_path)))).Wait()
    return str(extract_path)
    
def get_rf_fmt(rage_file: "YdrFile | YftFile") -> str | None:
    format: str = rage_file.Name.split('.')[1]
    if format:
        return format
    return None