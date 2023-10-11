import sys
import os
from .cw_image_tools import get_dds
from ...vicho_dependencies import DEPENDENCIES_INSTALLED
from .cw_py_misc import jenkhash

sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))


if DEPENDENCIES_INSTALLED:
    import clr

    clr.AddReference('CodeWalker.Core')
    clr.AddReference("System.Collections")
    from System.Collections.Generic import List
    from CodeWalker import GameFiles
    from CodeWalker import Utils 

    def TextureListFromDDSFiles(ddsFiles: list[str]) -> List[GameFiles.Texture]:
        textureList = List[GameFiles.Texture]()
        for ddsFile in ddsFiles:
            fn = ddsFile
            if not os.path.exists(fn):
                print("File not found: " + fn)
                continue
            try:
                with open(ddsFile, "rb") as dds_open:
                    content = dds_open.read()
                byte_array = bytearray(content)
                tex = Utils.DDSIO.GetTexture(byte_array)
                tex.Name = os.path.splitext(os.path.basename(ddsFile))[0]
                tex.NameHash = jenkhash(tex.Name.lower())
                textureList.Add(tex)
            except Exception as e:
                print(f"Error opening file {ddsFile}: {e}")
                continue
        return textureList

    def TexturesToYTD(textureList: List[GameFiles.Texture], ytdFile: GameFiles.YtdFile) -> GameFiles.YtdFile:
        textureDictionary = ytdFile.TextureDict
        textureDictionary.BuildFromTextureList(textureList)
        return ytdFile

    def ConvertFolderToYTD(folder: str) -> GameFiles.YtdFile:
        dds_files = get_dds(folder)
        ytd : GameFiles.YtdFile = GameFiles.YtdFile()
        ytd.TextureDict = GameFiles.TextureDictionary()
        final_ytd = TexturesToYTD(TextureListFromDDSFiles(dds_files), ytd)
        return final_ytd

