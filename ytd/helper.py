import shutil
import bpy
from bpy.app.handlers import persistent
from ..vicho_dependencies import dependencies_manager as d
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from CodeWalker.GameFiles import Texture, TextureDictionary, YtdFile
    from System.Collections.Generic import List
    from TeximpNet import Surface
    from TeximpNet.Compression import Compressor
import os
from .constants import SUPPORTED_FORMATS, ENV_TEXTURES
from pathlib import Path
from ..shared.funcs import get_files_by_ext, closest_pow2, closest_pow2_dims, calculate_mipmaps_lvls, get_random_string, delete_folder
from .image_info import ImageInfo
from ..shared.helper import abs_path, is_obj_in_any_collection, is_mesh, is_drawable, is_drawable_model
from ..shared.constants import YTD_SOLLUM_TYPES
from ..vicho_preferences import get_addon_preferences as prefs
from threading import Thread


def ytd_index_changed(self, context):
    if len(self.ytd_list) != 0:
        selected_item = self.ytd_list[self.ytd_active_index]
        self.mesh_list.clear()
        for mesh in selected_item.mesh_list:
            new_mesh = self.mesh_list.add()
            new_mesh.mesh = mesh.mesh


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
def update_post_ytd(scene, depsgraph):
    remove_invalid_meshes(scene)


def texture_list_from_dds_files(ddsFiles: list[str]) -> "List[Texture]":
    textureList: "List[gf.Texture]" = d.List[d.GameFiles.Texture]()
    for ddsFile in ddsFiles:
        fn = ddsFile
        if not os.path.exists(fn):
            print("File not found: " + fn)
            continue
        try:
            with open(ddsFile, "rb") as dds_open:
                content: bytes = dds_open.read()
            byte_array: bytearray = bytearray(content)
            tex: "gf.Texture" = d.Utils.DDSIO.GetTexture(byte_array)
            tex.Name = os.path.splitext(os.path.basename(ddsFile))[0]
            tex.NameHash = d.GameFiles.JenkHash.GenHash(str(tex.Name.lower()))
            d.GameFiles.JenkIndex.Ensure(tex.Name.lower())
            textureList.Add(tex)
        except Exception as e:
            print(f"Error opening file {ddsFile}: {e}")
            continue
    return textureList


def textures_to_ytd(textureList: "List[Texture]", ytdFile: "YtdFile"):
    textureDictionary: "TextureDictionary" = ytdFile.TextureDict
    textureDictionary.BuildFromTextureList(textureList)
    return ytdFile


def is_transparent(image: "Surface") -> bool:
    return image.IsTransparent


def convert_folder_to_ytd(folder: str):
    dds_files: list[str] = get_files_by_ext(folder, "dds")
    ytd: "YtdFile" = d.GameFiles.YtdFile()
    ytd.TextureDict = d.GameFiles.TextureDictionary()
    ytd.TextureDict.Textures = d.GameFiles.ResourcePointerList64[d.GameFiles.Texture]()
    ytd.TextureDict.TextureNameHashes = d.GameFiles.ResourceSimpleList64_uint()
    final_ytd: "YtdFile" = textures_to_ytd(texture_list_from_dds_files(dds_files), ytd)
    return final_ytd


def convert_img_to_dds(
    filepath: str,
    file_ext: str,
    quality: str,
    do_max_dimension: bool,
    half_res: bool,
    max_res: int,
    output_path: str,
    is_tint: bool,
    resize_dds: bool,
):
    adv = bpy.context.scene.ytd_advanced_mode
    surface: "Surface" = None
    compressor: "Compressor" = d.Compressor()

    img_filter: filter[str] = (
        filter(lambda x: x != ".dds", SUPPORTED_FORMATS)
        if not resize_dds
        else SUPPORTED_FORMATS
    )

    if file_ext in img_filter:
        try:
            print(f"Trying to load image {filepath}")
            surface: "Surface" = d.Surface.LoadFromFile(filepath, True)
        except Exception:
            print(f"Error loading image {filepath}")
            return None
    else:
        print(f"Invalid file extension {file_ext}")
        return None

    width: int = surface.Width
    height: int = surface.Height
    if adv:
        if do_max_dimension:
            width, height = closest_pow2_dims(width, height, max_res, False)
        if half_res:
            width, height = closest_pow2_dims(width, height, 0, True)
        if do_max_dimension or half_res:
            surface.Resize(width, height, d.ImageFilter.Lanczos3)
    else:
        width, height = closest_pow2(width), closest_pow2(height)
    mip_levels: int = calculate_mipmaps_lvls(width, height)
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


def get_images_info_from_mat(mat: bpy.types.Material, self=None) -> list[ImageInfo]:
    images_info: list[ImageInfo] = []
    if mat.use_nodes:
        mat_nodes = mat.node_tree.nodes
        match mat.sollum_type:
            case "sollumz_material_shader":
                for node in mat_nodes:
                    if node_is_image(node) and not is_sampler_embedded(node):
                        if is_img_valid(node.image):
                            images_info.append(
                                ImageInfo(
                                    abs_path(node.image.filepath),
                                    mat.name,
                                    is_tint_shader(node),
                                )
                            )
                        else:
                            self.report(
                                {"ERROR"},
                                f"Missing image?: {node.image} in material: {mat.name}",
                            )
            case "sollumz_material_none":
                for node in mat_nodes:
                    if node_is_image(node):
                        if is_img_valid(node.image):
                            images_info.append(
                                ImageInfo(abs_path(node.image.filepath), mat.name)
                            )
                        else:
                            self.report(
                                {"ERROR"},
                                f"Missing image?: {node.image} in material: {mat.name}",
                            )

    if prefs().skip_environment_textures:
        images_info = [
            img_inf
            for img_inf in images_info
            if img_inf.img_name.lower() not in ENV_TEXTURES
        ]

    return images_info


def is_img_valid(image: bpy.types.Image) -> bool:
    if image and os.path.exists(abs_path(image.filepath)):
        return True


def node_is_image(node) -> bool:
    return node.type == "TEX_IMAGE"


def is_sampler_embedded(node) -> bool:
    return node.texture_properties.embedded


def is_tint_shader(node) -> bool:
    return node.name == "TintPaletteSampler"


def create_texture_package_folder(ytd, ExportPath):
    folder_path = os.path.join(ExportPath, ytd.name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def mesh_list_from_objs(objects: list[bpy.types.Object]) -> list[bpy.types.Object]:
    new_mesh_list = []
    for obj in objects:
        if is_mesh(obj) or is_drawable_model(obj):
            new_mesh_list.append(obj)
        elif obj.sollum_type in filter(
            lambda x: x != "sollumz_drawable_model", YTD_SOLLUM_TYPES
        ):
            for draw_child in obj.children:
                if is_drawable(draw_child):
                    for model_child in draw_child.children:
                        if is_mesh(model_child) or is_drawable_model(model_child):
                            new_mesh_list.append(model_child)
                elif is_mesh(draw_child) and is_drawable_model(draw_child):
                    new_mesh_list.append(draw_child)
    return new_mesh_list


def add_ytd_to_list(scene, objs, ytd_list, self=None):
    objects = mesh_list_from_objs(objs)
    if not mesh_exist_in_ytd(scene, objects, self):
        item = scene.ytd_list.add()
        item.name = f"TextureDictionary{len(ytd_list)}"
        for obj in objects:
            item.mesh_list.add().mesh = obj
            self.report({"INFO"}, f"Added {obj.name} to {item.name}")
        return True


def add_meshes_to_ytd(index: int, objs, scene, self=None):
    objs = mesh_list_from_objs(objs)
    if not mesh_exist_in_ytd(scene, objs, self):
        for obj in objs:
            scene.ytd_list[index].mesh_list.add().mesh = obj
            self.report({"INFO"}, f"Added {obj.name} to {scene.ytd_list[index].name}")
        return True
    return False


def mesh_exist_in_ytd(scene, objs, self=None):
    for ytd in scene.ytd_list:
        for mesh in ytd.mesh_list:
            if mesh.mesh in objs:
                self.report(
                    {"ERROR"}, f"Mesh {mesh.mesh.name} already exists in {ytd.name}"
                )
                return True
    return False


def get_parent_from_sollumz_obj(obj):
    if obj.parent:
        obj_parent = obj.parent
        soll_type = obj_parent.sollum_type
        if soll_type == "sollumz_drawable":
            if obj_parent.parent:
                lvl2_parent = obj_parent.parent
                if lvl2_parent.sollum_type in [
                    "sollumz_drawable_dictionary",
                    "sollumz_fragment",
                ]:
                    return lvl2_parent
            else:
                return obj_parent


def auto_fill_ytd_field(scene, self):
    ytd_list = scene.ytd_list
    parents = []
    for ytd in ytd_list:
        for m in ytd.mesh_list:
            parent = get_parent_from_sollumz_obj(m.mesh)
            if parent:
                parents.append((parent, ytd.name))

    parents = set(parents)

    for ytyp in scene.ytyps:
        for arch in ytyp.archetypes:
            for p in parents:
                if arch.name == p[0].name:
                    arch.texture_dictionary = p[1]
                    self.report({"INFO"}, f"Auto-filled {arch.name} with {p[1]}")
                    continue


def update_img_data_list(item, self=None):
    item.img_data_list.clear()
    for mesh_obj in item.mesh_list:
        for mat in mesh_obj.mesh.material_slots:
            if mat.material:
                images: list[ImageInfo] = get_images_info_from_mat(mat.material, self)
                for img in images:
                    if img:
                        if img.img_name_full in [
                            img_data.img_name_full for img_data in item.img_data_list
                        ]:
                            continue
                        img_data = item.img_data_list.add()
                        img_data.img_path = img.img_path
                        img_data.img_ext = img.img_ext
                        img_data.img_name = img.img_name
                        img_data.img_name_full = img.img_name_full
                        img_data.flag_tint = img.flag_tint
                        img_data.flag_0 = img.flag_0
                        img_data.flag_1 = img.flag_1


def export_img_packages(
    package_list, export_path, quality, half_res, max_res, do_max_res, resize_dds, self
):
    scene = bpy.context.scene
    actually_resize: bool = (
        scene.max_pixel_size or scene.divide_textures_size and scene.ytd_advanced_mode
    )
    new_export_path = os.path.join(export_path, get_random_string())
    for pak in package_list:
        update_img_data_list(pak, self)
        print(f"YTD Item: {len(pak.img_data_list)}")
        ytd_folder = create_texture_package_folder(pak, new_export_path)
        threads = []
        for img in pak.img_data_list:
            if img.img_ext == ".dds":
                if resize_dds and actually_resize:
                    threads.append(
                        Thread(
                            target=convert_img_to_dds,
                            args=(
                                img.img_path,
                                img.img_ext,
                                quality,
                                do_max_res,
                                half_res,
                                max_res,
                                ytd_folder,
                                img.flag_tint,
                                resize_dds,
                            ),
                        )
                    )
                    threads[-1].start()
                else:
                    threads.append(
                        Thread(target=shutil.copy, args=(img.img_path, ytd_folder))
                    )
                    threads[-1].start()
            else:
                threads.append(
                    Thread(
                        target=convert_img_to_dds,
                        args=(
                            img.img_path,
                            img.img_ext,
                            quality,
                            do_max_res,
                            half_res,
                            max_res,
                            ytd_folder,
                            img.flag_tint,
                            False,
                        ),
                    )
                )
                threads[-1].start()
        for thread in threads:
            thread.join()
        ytd_file: "YtdFile" = convert_folder_to_ytd(ytd_folder)
        folder_path: Path = Path(ytd_folder)
        print(f"Folder Path: {folder_path.name}")
        output_file_path = Path(export_path) / f"{folder_path.name}.ytd"
        print(f"Output File Path: {output_file_path}")
        with open(f"{output_file_path}", "wb") as f:
            byte_array: bytearray = bytearray(list(ytd_file.Save()))
            f.write(byte_array)
    delete_folder(new_export_path)


def export_img_folders(package_list, export_path, self):
    rdm_folder = get_random_string()
    new_export_path = os.path.join(export_path, rdm_folder)
    for pak in package_list:
        update_img_data_list(pak, self)
        package_folder = create_texture_package_folder(pak, new_export_path)
        for img in pak.img_data_list:
            shutil.copy(img.img_path, package_folder)

    return rdm_folder

def update_ytd_path(self, context):
    """Update the YTD export path to be absolute."""
    if self.ytd_export_path != '':
        self.ytd_export_path = bpy.path.abspath(self.ytd_export_path)