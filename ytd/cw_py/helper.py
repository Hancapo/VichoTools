import math
from pathlib import Path
import os
from ...vicho_dependencies import dependencies_manager as d
from .misc import calculate_mipmaps_lvls, get_dds
from ...misc.funcs import power_of_two_resize

#sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))
SUPPORTED_FORMATS = [".png", ".jpg", ".bmp", ".tiff", ".tif", ".jpeg", ".dds", ".psd", ".gif", ".webp"]


def texture_list_from_dds_files(ddsFiles: list[str]):
    textureList = d.List[d.GameFiles.Texture]()
    for ddsFile in ddsFiles:
        fn = ddsFile
        if not os.path.exists(fn):
            print("File not found: " + fn)
            continue
        try:
            with open(ddsFile, "rb") as dds_open:
                content = dds_open.read()
            byte_array = bytearray(content)
            tex = d.Utils.DDSIO.GetTexture(byte_array)
            tex.Name = os.path.splitext(os.path.basename(ddsFile))[0]
            tex.NameHash = d.GameFiles.JenkHash.GenHash(str(tex.Name.lower()))
            d.GameFiles.JenkIndex.Ensure(tex.Name.lower())
            textureList.Add(tex)
        except Exception as e:
            print(f"Error opening file {ddsFile}: {e}")
            continue
    return textureList


def textures_to_ytd(textureList, ytdFile):
    textureDictionary = ytdFile.TextureDict
    textureDictionary.BuildFromTextureList(textureList)
    return ytdFile


def resize_image(image):
    imageHeight: int = image.Height
    imageWidth: int = image.Width
    log2Width: float = math.log2(imageWidth)
    log2Height: float = math.log2(imageHeight)
    if log2Width % 1 == 0 and log2Height % 1 == 0:
        return image
    image_new_size = power_of_two_resize(imageWidth, imageHeight)
    image.Resize(image_new_size[0], image_new_size[1], d.ImageFilter.Lanczos3)
    return image


def is_transparent(image) -> bool:
    return image.IsTransparent


def convert_folder_to_ytd(folder: str):
    dds_files = get_dds(folder)
    ytd = d.GameFiles.YtdFile()
    ytd.TextureDict = d.GameFiles.TextureDictionary()
    ytd.TextureDict.Textures = d.GameFiles.ResourcePointerList64[d.GameFiles.Texture]()
    ytd.TextureDict.TextureNameHashes = d.GameFiles.ResourceSimpleList64_uint()
    final_ytd = textures_to_ytd(texture_list_from_dds_files(dds_files), ytd)
    return final_ytd


def convert_img_to_dds(filepath: str):
    image = None
    compressor = d.Compressor()
    fileExt = Path(filepath).suffix
    fileName = Path(filepath).stem
    if fileExt in SUPPORTED_FORMATS:
        try:
            image = d.Surface.LoadFromFile(filepath)
        except Exception:
            print(f"Error loading image {filepath}")
            return None
    else:
        print(f"Invalid file extension {fileExt}")
        return None
    
    resized_image = resize_image(image)
    resized_image.FlipVertically()
    height = resized_image.Height
    width = resized_image.Width
    mip_levels = calculate_mipmaps_lvls(width, height)
    
    compressor.Input.SetData(resized_image)
    compressor.Input.SetMipmapGeneration(True, mip_levels)
    compressor.Input.MipmapFilter = d.MipmapFilter.Box
    compressor.Output.OutputFileFormat = d.OutputFileFormat.DDS
    compressor.Compression.Quality = d.CompressionQuality.Normal
    
    compressor.Compression.Format = d.CompressionFormat.DXT5 if is_transparent(resized_image) else d.CompressionFormat.DXT1
    
    output_path = os.path.join(os.path.dirname(filepath), f"{fileName}.dds")
    
    compressor.Process(output_path)
    
    image.Dispose()
    resized_image.Dispose()
    compressor.Dispose()
    
    
