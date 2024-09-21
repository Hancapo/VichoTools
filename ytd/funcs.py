import os
from pathlib import Path
import shutil
from ..vicho_preferences import get_addon_preferences as prefs
from .constants import COMPAT_SOLL, ENV_TEXTURES, ARCH_TYPES
from .helper import convert_folder_to_ytd, convert_img_to_dds
from .image_info import ImageInfo
import bpy
from ..misc.funcs import is_drawable_model, is_mesh, is_drawable, gen_rdm_str


def get_images_info_from_mat(mat, self = None) -> list[ImageInfo]:
    images_info: list[ImageInfo] = []
    if mat.use_nodes:
        mat_nodes = mat.node_tree.nodes
        match mat.sollum_type:
            case "sollumz_material_shader":
                for node in mat_nodes:
                    if node_is_image(node) and not is_sampler_embedded(node) and is_valid_image(node.image):
                        images_info.append(ImageInfo(node.image, mat.name, is_tint_shader(node)))
            case "sollumz_material_none":
                for node in mat_nodes:
                    if node_is_image(node) and is_valid_image(node.image):
                        images_info.append(ImageInfo(node.image, mat.name))
    
    if prefs().skip_environment_textures:
        images_info = [img_inf for img_inf in images_info if img_inf.image_name.lower() not in ENV_TEXTURES]
        
    if(check_if_images_exists(images_info, self)):
        return images_info

def is_valid_image(image) -> bool:
    if image and image.has_data:
        return True

def check_if_images_exists(img_list, self = None) -> bool:
    for img_info in img_list:
        if is_valid_image(img_info.image):
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

def is_obj_type(obj, obj_type) -> bool:
    return obj.type == obj_type

def create_texture_package_folder(ytd, ExportPath, self=None):
    folder_path = os.path.join(ExportPath, ytd.name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def delete_folder(path):
    shutil.rmtree(path)

def mesh_list_from_objs(objects):
    new_mesh_list = []
    for obj in objects:
        if is_mesh(obj) or is_drawable_model(obj):
            new_mesh_list.append(obj)
        elif obj.sollum_type in filter(lambda x: x != "sollumz_drawable_model", COMPAT_SOLL):
            for draw_child in obj.children:
                if is_drawable(draw_child):
                    for model_child in draw_child.children:
                        if (
                            is_mesh(model_child)
                            or is_drawable_model(model_child)
                        ):
                            new_mesh_list.append(model_child)
                elif (
                    is_mesh(draw_child)
                    and is_drawable_model(draw_child)
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


def get_parent_from_sollumz_obj(obj):
    if obj.parent:
        obj_parent = obj.parent
        soll_type = obj_parent.sollum_type
        if soll_type == 'sollumz_drawable':
            if obj_parent.parent:
                lvl2_parent = obj_parent.parent
                if lvl2_parent.sollum_type in ['sollumz_drawable_dictionary', 'sollumz_fragment']:
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


def update_img_data_list(item, self = None):
    item.img_data_list.clear()
    for mesh_obj in item.mesh_list:
            for mat in mesh_obj.mesh.material_slots:
                if mat.material:
                    images = get_images_info_from_mat(mat.material, self)
                    for img in images:
                        img_data = item.img_data_list.add()
                        img_data.img_texture = img.image
                        img_data.flag_tint = img.flag_tint
                        img_data.flag_0 = img.flag_0
                        img_data.flag_1 = img.flag_1
        
        
def export_img_packages(package_list, export_path, self, quality, half_res, max_res, do_max_res, resize_dds):
    scene = bpy.context.scene
    actually_resize: bool = scene.max_pixel_size or scene.divide_textures_size and scene.ytd_advanced_mode
    new_export_path = os.path.join(export_path, gen_rdm_str())
    for pak in package_list:
        update_img_data_list(pak, self)
        print(f"YTD Item: {len(pak.img_data_list)}")
        ytd_folder = create_texture_package_folder(pak, new_export_path)
        for img in pak.img_data_list:
            image_path = bpy.path.abspath(img.img_texture.filepath)
            image_format = Path(image_path).suffix
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
        output_file_path = Path(export_path) / f"{folder_path.name}.ytd"
        print(f"Output File Path: {output_file_path}")
        with open(f"{output_file_path}", "wb") as f:
            bytes_data = ytd_file.Save()
            byte_array = bytearray(list(bytes_data))
            f.write(byte_array)
    delete_folder(new_export_path)

def export_img_folders(package_list, export_path, self):
    rdm_folder = gen_rdm_str()
    new_export_path = os.path.join(export_path, rdm_folder)
    for pak in package_list:
        update_img_data_list(pak, self)
        package_folder = create_texture_package_folder(pak, new_export_path)
        for img in pak.img_data_list:
            image_path = bpy.path.abspath(img.img_texture.filepath)
            shutil.copy(image_path, package_folder)
    
    return rdm_folder