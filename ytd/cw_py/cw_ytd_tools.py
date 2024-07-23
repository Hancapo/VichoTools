import math
from pathlib import Path
import sys
import os
from ...vicho_dependencies import dependencies_manager as d
from .cw_py_misc import calculate_mipmaps, get_dds
from ...misc.misc_funcs import power_of_two_resize
sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))

valid_exts = [".png", ".jpg", ".bmp", ".tiff", ".tif", ".jpeg", ".dds"]


def texture_list_from_dds_files(ddsFiles: list[str]):
    if not d.available:
        return None
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
    if not d.available:
        return None
    textureDictionary = ytdFile.TextureDict
    textureDictionary.BuildFromTextureList(textureList)
    return ytdFile

def resize_image(image):
    if not d.available:
        return None
    imageHeight: int = image.GetMetadata().Height
    imageWidth: int = image.GetMetadata().Width
    log2Width: float = math.log2(imageWidth)
    log2Height: float = math.log2(imageHeight)
    if log2Width % 1 == 0 and log2Height % 1 == 0:
        return image
    
    image_new_size = power_of_two_resize(imageWidth, imageHeight)
    resized_image = image.Resize(0, image_new_size[0], image_new_size[1], d.TEX_FILTER_FLAGS.LINEAR)
    return resized_image
    
def is_transparent(image) -> bool:
    if not d.available:
        return None
    return not image.IsAlphaAllOpaque()
    
def convert_folder_to_ytd(folder: str):
    if not d.available:
        return None
    dds_files = get_dds(folder)
    ytd = d.GameFiles.YtdFile()
    ytd.TextureDict = d.GameFiles.TextureDictionary()
    ytd.TextureDict.Textures = d.GameFiles.ResourcePointerList64[d.GameFiles.Texture]()
    ytd.TextureDict.TextureNameHashes = d.GameFiles.ResourceSimpleList64_uint()
    final_ytd = textures_to_ytd(texture_list_from_dds_files(dds_files), ytd)
    return final_ytd

def convert_img_to_dds(filepath : str):
    if not d.available:
        return None
    image = None
    fileExt = Path(filepath).suffix
    fileName = Path(filepath).stem
    if fileExt in valid_exts:
        try:
            image = d.TexHelper.Instance.LoadFromWICFile(filepath, d.WIC_FLAGS.NONE)
        except:
            print(f"Error loading image {filepath}")
            return None
    elif fileExt == ".tga":
        try:
            image = d.TexHelper.Instance.LoadFromTGAFile(filepath)
        except:
            print(f"Error loading image {filepath}")
            return None
    else:
        print(f"Invalid file extension {fileExt}")
        return None
    resized_image = resize_image(image)
    height = resized_image.GetMetadata().Height
    width = resized_image.GetMetadata().Width
    mip_maps_levels = calculate_mipmaps(width, height)
    mipmapped_image = resized_image.GenerateMipMaps(d.TEX_FILTER_FLAGS.BOX, mip_maps_levels) if mip_maps_levels > 1 else resized_image
    compressed_image = mipmapped_image.Compress(d.DXGI_FORMAT.BC3_UNORM, d.TEX_COMPRESS_FLAGS.SRGB, 0) if is_transparent(mipmapped_image) else mipmapped_image.Compress(d.DXGI_FORMAT.BC1_UNORM, d.TEX_COMPRESS_FLAGS.SRGB, 0.5)
    output_path = os.path.join(os.path.dirname(filepath), f"{fileName}.dds")
    compressed_image.SaveToDDSFile(d.DDS_FLAGS.NONE, output_path)

