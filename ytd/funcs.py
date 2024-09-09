import os
from pathlib import Path
import shutil
from .cw_py.misc import get_folder_list_from_dir
from .cw_py.helper import convert_folder_to_ytd, convert_img_to_dds
from ..vicho_preferences import get_addon_preferences as prefs
from .helper import COMPAT_SOLL
from .image_info import ImageInfo
import bpy

ENV_TEXTURES = [
    "env_bark",
    "env_cloth",
    "env_crusty",
    "env_noise_concrete",
    "env_noise_heavy",
    "env_smooth_concrete2",
    "env_stucco",
    "env_woodgrain",
    "env_woodgrain_2",
]


def get_images_info_from_mat(mat, self = None) -> list[ImageInfo]:
    images_info: list[ImageInfo] = []
    if mat.use_nodes:
        mat_nodes = mat.node_tree.nodes
        match mat.sollum_type:
            case "sollumz_material_shader":
                for node in mat_nodes:
                    if node_is_image(node) and not is_sampler_embedded(node):
                        images_info.append(ImageInfo(node.image, mat.name, is_tint_shader(node)))
            case "sollumz_material_none":
                for node in mat_nodes:
                    if node_is_image(node):
                        images_info.append(ImageInfo(node.image, mat.name))
    
    if prefs().skip_environment_textures:
        images_info = [img_inf for img_inf in images_info if img_inf.image_name.lower() not in ENV_TEXTURES]
        
    if(check_if_images_exists(images_info, self)):
        return images_info

def check_if_images_exists(img_list, self = None) -> bool:
    for img_info in img_list:
        print(Path(img_info.image_path))
        if Path(img_info.image_path).is_file():
            continue
        else:
            self.report({"ERROR"}, f"Missing image named [{img_info.image_name}] from [{img_info.material}] material")
            return False
    return True

def node_is_image(node) -> bool:
    return node.type == "TEX_IMAGE"

def is_sampler_embedded(node) -> bool:
    return node.texture_properties.embedded

def is_tint_shader(node) -> bool:
    return node.name == "TintPaletteSampler"

def is_sollum_draw_model(obj) -> bool:
    return obj.sollum_type == "sollumz_drawable_model"

def is_obj_type(obj, obj_type) -> bool:
    return obj.type == obj_type

def create_ytd_folder(ytd, ExportPath, self=None):
    folder_path = os.path.join(ExportPath, ytd.name)
    print(f"Added folder {folder_path}")
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def delete_folders(FolderList, ExportPath):
    for folder in FolderList:
        folder_path = os.path.join(ExportPath, folder.name)
        shutil.rmtree(folder_path)


def mesh_list_from_objs(objects):
    new_mesh_list = []
    for obj in objects:
        if obj.type == "MESH" or obj.sollum_type == "sollumz_drawable_model":
            new_mesh_list.append(obj)
        elif obj.sollum_type in filter(lambda x: x != "sollumz_drawable_model", COMPAT_SOLL):
            for draw_child in obj.children:
                if draw_child.sollum_type == "sollumz_drawable":
                    for model_child in draw_child.children:
                        if (
                            model_child.type == "MESH"
                            or model_child.sollum_type == "sollumz_drawable_model"
                        ):
                            new_mesh_list.append(model_child)
                elif (
                    draw_child.type == "MESH"
                    and draw_child.sollum_type == "sollumz_drawable_model"
                ):
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


def auto_fill_ytd_field(scene, self):
    ytd_list = scene.ytd_list
    for ytyp in scene.ytyps:
        for arch in ytyp.archetypes:
            if arch.type not in ["sollumz_archetype_base", "sollumz_archetype_time"]:
                continue
            for ytd in ytd_list:
                for m in ytd.mesh_list:
                    mesh = m.mesh
                    if mesh.sollum_type != "sollumz_drawable_model":
                        continue
                    if mesh.parent.sollum_type != "sollumz_drawable":
                        continue
                    if mesh.parent.name != arch.asset_name:
                        continue
                    arch.texture_dictionary = ytd.name
                    self.report({"INFO"}, f"Assigned {ytd.name} to {arch.asset_name}")


def update_img_data_list(item, self = None):
    item.img_data_list.clear()
    for mesh_obj in item.mesh_list:
            for mat in mesh_obj.mesh.material_slots:
                if mat.material:
                    images = get_images_info_from_mat(mat.material, self)
                    print(f"Images: {images}")
                    for img in images:
                        img_data = item.img_data_list.add()
                        img_data.img_texture = img.image
                        img_data.flag_tint = img.flag_tint
                        img_data.flag_0 = img.flag_0
                        img_data.flag_1 = img.flag_1
        
        
def export_ytd_files(FolderList, ExportPath, self, quality, half_res, max_res, do_max_res, resize_dds):
    scene = bpy.context.scene
    actually_resize: bool = scene.max_pixel_size or scene.divide_textures_size and scene.ytd_advanced_mode
    newExportPath = os.path.join(ExportPath, "output")
    for ytd_item in FolderList:
        update_img_data_list(ytd_item, self)
        print(f"YTD Item: {len(ytd_item.img_data_list)}")
        ytd_folder = create_ytd_folder(ytd_item, newExportPath)
        for img in ytd_item.img_data_list:
            image_format = Path(img.img_texture.filepath).suffix
            image_path = bpy.path.abspath(img.img_texture.filepath)
            if image_format == ".dds":
                if resize_dds and actually_resize:
                    convert_img_to_dds(image_path, image_format, quality, do_max_res, half_res, max_res, ytd_folder, img.flag_tint, resize_dds)
                else:
                    shutil.copy(image_path, ytd_folder)
            else:
                convert_img_to_dds(image_path, image_format, quality, do_max_res, half_res, max_res, ytd_folder, img.flag_tint, False)
        ytd_file = convert_folder_to_ytd(ytd_folder)
        folder_path = Path(ytd_folder)
        print(f"Folder Path: {folder_path.name}")
        output_file_path = Path(newExportPath) / f"{folder_path.name}.ytd"
        print(f"Output File Path: {output_file_path}")
        with open(f"{output_file_path}", "wb") as f:
            bytes_data = ytd_file.Save()
            byte_array = bytearray(list(bytes_data))
            f.write(byte_array)
        delete_folders(FolderList, newExportPath)
        