import bpy
from bpy.app.handlers import persistent
from ..vicho_dependencies import dependencies_manager as d
import os
from .constants import SUPPORTED_FORMATS
from pathlib import Path
from .misc import get_dds, closest_pow2, closest_pow2_dims, calculate_mipmaps_lvls

def ytd_index_changed(self, context):
    if len(self.ytd_list) != 0:
        selected_item = self.ytd_list[self.ytd_active_index]
        self.mesh_list.clear()
        for mesh in selected_item.mesh_list:
            new_mesh = self.mesh_list.add()
            new_mesh.mesh = mesh.mesh


def is_obj_in_any_collection(obj):
    return any(obj.name in collection.objects for collection in bpy.data.collections)


def remove_invalid_meshes(scene):
    for ytd_index in reversed(range(len(scene.ytd_list))):
        ytd = scene.ytd_list[ytd_index]
        for mesh_index, mesh in reversed(list(enumerate(ytd.mesh_list))):
            if mesh.mesh is None or (
                mesh.mesh.name not in bpy.context.view_layer.objects
                and not is_obj_in_any_collection(mesh.mesh)
            ):
                if (
                    mesh.mesh
                    and mesh.mesh.name not in bpy.context.view_layer.objects
                    and not is_obj_in_any_collection(mesh.mesh)
                ):
                    bpy.data.objects.remove(mesh.mesh, do_unlink=True)
                ytd.mesh_list.remove(mesh_index)
                switch_ytd_selected_index(scene)

        if len(ytd.mesh_list) == 0:
            scene.ytd_list.remove(ytd_index)
            switch_ytd_selected_index(scene)


def switch_ytd_selected_index(scene):
    if len(scene.ytd_list) != 0:
        if len(scene.ytd_list[scene.ytd_active_index].mesh_list) < 1:
            scene.ytd_active_index = 0 if len(scene.ytd_list) > 0 else -1


@persistent
def update_post(scene, depsgraph):
    remove_invalid_meshes(scene)

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


def convert_img_to_dds(filepath: str, file_ext: str, quality: str, do_max_dimension: bool, half_res: bool, max_res: int, output_path: str, is_tint: bool, resize_dds: bool):
    adv = bpy.context.scene.ytd_advanced_mode
    surface = None
    compressor = d.Compressor()
    
    img_filter = filter(lambda x: x != ".dds", SUPPORTED_FORMATS) if not resize_dds else SUPPORTED_FORMATS
    
    if file_ext in img_filter:
        try:
            print(f"Trying to load image {filepath}")
            surface = d.Surface.LoadFromFile(filepath, True)
        except Exception:
            print(f"Error loading image {filepath}")
            return None
    else:
        print(f"Invalid file extension {file_ext}")
        return None

    width, height = surface.Width, surface.Height
    if adv:
        if do_max_dimension:
            width, height = closest_pow2_dims(width, height, max_res, False)
        if half_res:
            width, height = closest_pow2_dims(width, height, 0, True)
        if do_max_dimension or half_res:
            surface.Resize(width, height, d.ImageFilter.Lanczos3)
    else:
        width, height = closest_pow2(width), closest_pow2(height)
    mip_levels = calculate_mipmaps_lvls(width, height)
    compressor.Input.SetData(surface)
    compressor.Input.RoundMode = d.RoundMode.ToNearestPowerOfTwo
    if is_tint:
        compressor.Input.SetMipmapGeneration(False, 1)
        compressor.Compression.Format = d.CompressionFormat.BGRA
        
    else:
        compressor.Input.SetMipmapGeneration(True, mip_levels)
        compressor.Compression.Format = (
            d.CompressionFormat.DXT5
            if is_transparent(surface)
            else d.CompressionFormat.DXT1a
        )

    compressor.Compression.Quality = get_quality(quality)
    dds_name = os.path.join(output_path, Path(filepath).stem + ".dds")
    compressor.Process(dds_name)
    surface.Dispose()
    compressor.Dispose()


def get_quality(quality: str):
    match quality:
        case "FASTEST":
            return d.CompressionQuality.Fastest
        case "NORMAL":
            return d.CompressionQuality.Normal
        case "PRODUCTION":
            return d.CompressionQuality.Production
        case "HIGHEST":
            return d.CompressionQuality.Highest
        case _:
            return d.CompressionQuality.Normal