import shutil
from typing import NamedTuple
import bpy
from bpy.app.handlers import persistent
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from bpy.types import Nodes, Material, Image, ShaderNode, Object, Scene

from ..shared.constants import YTD_SOLLUM_TYPES
from ..shared.funcs import (
    delete_folder,
    get_random_string,
)
from ..shared.helper import (
    abs_path,
    is_drawable,
    is_drawable_model,
    is_mesh,
    is_obj_in_any_collection,
)
from ..vicho_preferences import get_addon_preferences as prefs
from .constants import ENV_TEXTURES, SUPPORTED_FORMATS
from .image_info import ImageInfo
from texfury import Texture, image_dimensions, BCFormat, suggest_format, has_transparency, fit_dimensions, create_dict_from_folder


class ExportableItdInfo(NamedTuple):
    dds_conv_quality: str
    game_target: str
    max_pixel_size: str | int
    adv_toggle: bool
    

def itd_index_changed(self, context):
    if len(self.itd_list) != 0:
        selected_item = self.itd_list[self.itd_active_index]
        self.mesh_list.clear()
        for mesh in selected_item.mesh_list:
            new_mesh = self.mesh_list.add()
            new_mesh.mesh = mesh.mesh


def remove_invalid_meshes(scene):
    for ytd_index in reversed(range(len(scene.itd_list))):
        ytd = scene.itd_list[ytd_index]
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
                switch_itd_selected_index(scene)

        if len(ytd.mesh_list) == 0:
            scene.itd_list.remove(ytd_index)
            switch_itd_selected_index(scene)


def switch_itd_selected_index(scene):
    if len(scene.itd_list) != 0:
        if len(scene.itd_list[scene.itd_active_index].mesh_list) < 1:
            scene.itd_active_index = 0 if len(scene.itd_list) > 0 else -1


@persistent
def update_post_itd(scene, depsgraph):
    remove_invalid_meshes(scene)

def convert_img_to_dds(itd_data: ExportableItdInfo, output_path: Path, is_tint: bool, resize_dds: bool, file_ext: str, filepath: Path) -> bool:
    tex: Texture = None

    max_res: int | None = None if itd_data.max_pixel_size == "NO_LIMIT" else int(itd_data.max_pixel_size)
    
    img_filter: filter[str] = (
        filter(lambda x: x != ".dds", SUPPORTED_FORMATS)
        if not resize_dds
        else SUPPORTED_FORMATS
    )


    if file_ext in img_filter:
        try:
            width, height, _ = image_dimensions(filepath)
            print(f"Trying to load image {filepath}")
            if itd_data.adv_toggle and max_res is not None:
                width, height = fit_dimensions(width, height, max_res)
            detected_format: BCFormat = BCFormat.A8R8G8B8 if is_tint else suggest_format(has_transparency(filepath), quality_over_size=False)

            if file_ext == '.dds':
                tex = Texture.from_dds(filepath)
                if resize_dds and tex:
                    tex.resize(width, height)
            else:
                tex = Texture.from_image(source=filepath, format=detected_format, quality=float(itd_data.dds_conv_quality), generate_mipmaps=not is_tint, max_size=max_res)

            
            dds_path = output_path / f"{Path(filepath).stem}.dds"
            tex.save_dds(dds_path)
            return True

        except Exception:
            print(f"Error loading image {filepath}")
            return False
        
    return False

def build_images_list_from_mat(mat: Material, self=None) -> list[ImageInfo]:
    images_info: list[ImageInfo] = []

    if not mat.use_nodes:
        return images_info
    
    mat_nodes: Nodes = mat.node_tree.nodes
    for node in mat_nodes:

        if not is_image_node(node):
            continue
        
        if is_img_valid(node.image):
            img: Image = node.image
            if not is_sampler_embedded(node):
                images_info.append(ImageInfo(
                    None if is_img_packed(img) else abs_path(img.filepath),
                    mat.name,
                    is_tint_shader(node)
                ))
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


def is_img_valid(image: Image | None) -> bool:
    if not image:
        return False

    if image.packed_file:
        return True

    return os.path.exists(abs_path(image.filepath))


def is_img_packed(image: Image) -> bool:
    return bool(image and image.packed_file)


def is_image_node(node: bpy.types.Node | None) -> bool:
    return bool(node and node.bl_idname == "ShaderNodeTexImage")


def is_sampler_embedded(node: ShaderNode | None) -> bool:
    texture_properties = getattr(node, "texture_properties", None)
    return getattr(texture_properties, "embedded", False)


def is_tint_shader(node: ShaderNode | None) -> bool:
    return node.name == "TintPaletteSampler"


def create_package_folder(itd, export_path: str | Path) -> Path:
    folder_path = Path(export_path) / itd.name
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path


def mesh_list_from_objs(objects: list[Object]) -> list[Object]:
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


def add_itd_to_list(scene, objs, ytd_list, self=None):
    objects = mesh_list_from_objs(objs)
    if not mesh_exist_in_itd(scene, objects, self):
        item = scene.itd_list.add()
        item.name = f"TextureDictionary{len(ytd_list)}"
        for obj in objects:
            item.mesh_list.add().mesh = obj
            self.report({"INFO"}, f"Added {obj.name} to {item.name}")
        return True


def add_meshes_to_itd(index: int, objs, scene, self=None):
    objs = mesh_list_from_objs(objs)
    if not mesh_exist_in_itd(scene, objs, self):
        for obj in objs:
            scene.itd_list[index].mesh_list.add().mesh = obj
            self.report({"INFO"}, f"Added {obj.name} to {scene.itd_list[index].name}")
        return True
    return False


def mesh_exist_in_itd(scene, objs, self=None):
    for ytd in scene.itd_list:
        for mesh in ytd.mesh_list:
            if mesh.mesh in objs:
                self.report(
                    {"ERROR"}, f"Mesh {mesh.mesh.name} already exists in {ytd.name}"
                )
                return True
    return False


def get_parent_from_sollumz_obj(obj: Object) -> Object | None:
    if obj.parent:
        obj_parent: Object = obj.parent
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


def auto_fill_ytd_field(scene: Scene, self) -> None:
    itd_list = scene.itd_list
    parents: list[Object] = []
    for itd in itd_list:
        for m in itd.mesh_list:
            parent = get_parent_from_sollumz_obj(m.mesh)
            if parent:
                parents.append((parent, itd.name))

    parents = set(parents)

    for ytyp in scene.ytyps:
        for arch in ytyp.archetypes:
            for p in parents:
                if arch.name == p[0].name:
                    arch.texture_dictionary = p[1]
                    self.report({"INFO"}, f"Auto-filled {arch.name} with {p[1]}")
                    continue

def update_img_data_list(item, self=None) -> None:
    item.img_data_list.clear()
    for mesh_obj in item.mesh_list:
        for mat in mesh_obj.mesh.material_slots:

            if not mat.material:
                continue
            
            for img in build_images_list_from_mat(mat.material, self):
                if img.img_name_full not in [img_data.img_name_full for img_data in item.img_data_list]:
                    img_data = item.img_data_list.add()
                    img_data.img_path = img.img_path
                    img_data.img_ext = img.img_ext
                    img_data.img_name = img.img_name
                    img_data.img_name_full = img.img_name_full
                    img_data.flag_tint = img.flag_tint
                    img_data.flag_0 = img.flag_0
                    img_data.flag_1 = img.flag_1


def export_img_packages(itd_list, path: Path, resize_dds: bool, self) -> None:
    random_folder_path: Path = Path(path) / get_random_string()
    for itd in itd_list:
        update_img_data_list(itd, self)
        itd_folder: Path = create_package_folder(itd, random_folder_path)
        futures = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            for image in itd.img_data_list:
                if not resize_dds and image.img_ext == ".dds":
                    futures.append(executor.submit(shutil.copy, image.img_path, itd_folder))
                    continue
                itd_data = ExportableItdInfo(itd.dds_conv_quality, itd.game_target, itd.max_pixel_size, itd.adv_toggle)
                futures.append(executor.submit(convert_img_to_dds, itd_data, itd_folder, image.flag_tint, resize_dds, image.img_ext, image.img_path))
        for future in as_completed(futures):
                    future.result()
        td_file_path: Path = Path(path) / f"{itd.name}.ytd"
        create_dict_from_folder(itd_folder, td_file_path)
    
    delete_folder(random_folder_path)


def export_img_folders(package_list, export_path, self) -> str:
    rdm_folder = get_random_string()
    new_export_path = os.path.join(export_path, rdm_folder)
    for pak in package_list:
        update_img_data_list(pak, self)
        package_folder = create_package_folder(pak, new_export_path)
        for img in pak.img_data_list:
            shutil.copy(img.img_path, package_folder)

    return rdm_folder


def update_itd_path(self, context) -> None:
    """Update the YTD export path to be absolute."""
    if self.itd_export_path != "":
        self.itd_export_path = bpy.path.abspath(self.itd_export_path)

def update_dds_quality(self, context) -> None:
    value = round(self.dds_conv_quality, 1)
    self.dds_conv_quality = max(0.1, min(1.0, value))