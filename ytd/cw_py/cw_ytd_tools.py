import sys
import os
from ...vicho_dependencies import depen_installed
from .cw_py_misc import jenkhash, calculate_mipmaps, get_dds, has_transparency

sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))


if depen_installed():
    import clr
    clr.AddReference('CodeWalker.Core')
    clr.AddReference("System.Collections")
    from System.Collections.Generic import List
    from CodeWalker import GameFiles
    from CodeWalker import Utils
    from wand.image import Image


    def texture_list_from_dds_files(ddsFiles: list[str]) -> List[GameFiles.Texture]:
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

    def textures_to_ytd(textureList: List[GameFiles.Texture], ytdFile: GameFiles.YtdFile) -> GameFiles.YtdFile:
        textureDictionary = ytdFile.TextureDict
        textureDictionary.BuildFromTextureList(textureList)
        return ytdFile

    def convert_folder_to_ytd(folder: str) -> GameFiles.YtdFile:
        dds_files = get_dds(folder)
        ytd : GameFiles.YtdFile = GameFiles.YtdFile()
        ytd.TextureDict = GameFiles.TextureDictionary()
        final_ytd = textures_to_ytd(texture_list_from_dds_files(dds_files), ytd)
        return final_ytd

    def convert_img_to_dds(filepath : str):
        with Image(filename=filepath) as image:
            with image.convert('dds') as converted:
                converted.options['dds:mipmaps'] = str(
                    calculate_mipmaps(image.width, image.height))
                transparent = has_transparency(image)
                if transparent:
                    converted.options['dds:compression'] = 'dxt5'
                else:
                    converted.options['dds:compression'] = 'dxt1'
                converted.save(filename=f'{os.path.splitext(filepath)[0]}.dds')

