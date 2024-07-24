import os
from pathlib import Path
import shutil
import bpy
from .cw_py.misc import get_folder_list_from_dir, get_non_dds
from ..vicho_dependencies import dependencies_manager as d

from .cw_py.helper import convert_folder_to_ytd, convert_img_to_dds

def get_images_from_material(material):
    images = []
    if material != None and material.use_nodes:
        material_nodes = material.node_tree.nodes
        match material.sollum_type:
            case 'sollumz_material_shader':
                for node in material_nodes:
                    if node_is_image(node) and not is_sampler_embedded(node):
                        images.append(node.image)
            case 'sollumz_material_none':
                for node in material_nodes:
                    if node_is_image(node):
                        images.append(node.image)
    return images

def node_is_image(node):
    return node.type == 'TEX_IMAGE'

def is_sampler_embedded(node):
    return node.texture_properties.embedded

def create_ytd_folders(FolderList, ExportPath, self):
    for folder in FolderList:
        update_material_list(folder)
        folder_path = os.path.join(ExportPath, folder.name)
        print(f'Added folder {folder_path}')
        os.makedirs(folder_path, exist_ok=True)
        for material_prop in folder.material_list:
            material = material_prop.material
            images = get_images_from_material(material)
            for img in images:
                if img:
                    image_path = bpy.path.abspath(img.filepath)
                    image_name = os.path.basename(image_path)
                    try:
                        shutil.copy(image_path, folder_path)
                    except FileNotFoundError:
                        self.report(
                            {'ERROR'}, f"Missing image named [{image_name}] from [{material.name}] material")
                        raise Exception(f"Missing image in [{folder.name}] YTD") from None


def delete_folders(FolderList, ExportPath):
    for folder in FolderList:
        folder_path = os.path.join(ExportPath, folder.name)
        shutil.rmtree(folder_path)


def image_objects_from_objects(objs):
    image_objects = set()
    for obj in objs:
        if obj.mesh.type != 'MESH':
            continue
        for material_prop in obj.mesh.material_slots:
            material = material_prop.material
            images = get_images_from_material(material)
            for img in images:
                if img:
                    image_objects.add(img)
    return list(image_objects)


def mesh_list_from_objects(objects):
    new_mesh_list = []
    for obj in objects:
        if obj.type == 'MESH' or obj.sollum_type == 'sollumz_drawable_model':
            new_mesh_list.append(obj)
        elif obj.sollum_type in ['sollumz_drawable', 'sollumz_drawable_dictionary', 'sollumz_fragment']:
            for draw_child in obj.children:
                if draw_child.sollum_type == 'sollumz_drawable':
                    for model_child in draw_child.children:
                        if model_child.type == 'MESH' or model_child.sollum_type == 'sollumz_drawable_model':
                            new_mesh_list.append(model_child)
                elif draw_child.type == 'MESH' and draw_child.sollum_type == 'sollumz_drawable_model':
                    new_mesh_list.append(draw_child)
    return new_mesh_list


def add_ytd_to_list(scene, objs, ytd_list, self=None):

    objects = mesh_list_from_objects(objs)

    if not mesh_exist_in_ytd(scene, objects, self):
        item = scene.ytd_list.add()
        item.name = f"TextureDictionary{len(ytd_list)}"
        for obj in objects:
            item.mesh_list.add().mesh = obj
            self.report({'INFO'}, f"Added {obj.name} to {item.name}")
        for obj in item.mesh_list:
            for slot in obj.mesh.material_slots:
                if slot.material:
                    item.material_list.add().material = slot.material
        return True


def add_meshes_to_ytd(index: int, objects, scene, self=None):
    objects = mesh_list_from_objects(objects)
    if not mesh_exist_in_ytd(scene, objects, self):
        for obj in objects:
            scene.ytd_list[index].mesh_list.add().mesh = obj
            self.report(
                {'INFO'}, f'Added {obj.name} to {scene.ytd_list[index].name}')
        return True
    return False


def mesh_exist_in_ytd(scene, objs, self=None):
    for ytd in scene.ytd_list:
        for mesh in ytd.mesh_list:
            if mesh.mesh in objs:
                self.report(
                    {'ERROR'}, f"Mesh {mesh.mesh.name} already exists in {ytd.name}")
                return True
    return False


def auto_fill_ytd_field(scene, self):
    ytd_list = scene.ytd_list
    for ytyp in scene.ytyps:
        for arch in ytyp.archetypes:
            if arch.type not in ['sollumz_archetype_base', 'sollumz_archetype_time']:
                continue
            for ytd in ytd_list:
                for m in ytd.mesh_list:
                    mesh = m.mesh
                    if mesh.sollum_type != 'sollumz_drawable_model':
                        continue
                    if mesh.parent.sollum_type != 'sollumz_drawable':
                        continue
                    if mesh.parent.name != arch.asset_name:
                        continue
                    arch.texture_dictionary = ytd.name
                    self.report({'INFO'}, f"Assigned {ytd.name} to {arch.asset_name}")

def update_material_list(item):
    item.material_list.clear()
    for obj in item.mesh_list:
        for slot in obj.mesh.material_slots:
            if slot.material:
                item.material_list.add().material = slot.material

def export_ytd_files(FolderList, ExportPath, self):
    print(f'Export path: {ExportPath}')
    newExportPath = os.path.join(ExportPath, 'output')
    create_ytd_folders(FolderList, newExportPath, self)
    folders = get_folder_list_from_dir(newExportPath)
    for folder in folders:
        for img in get_non_dds(folder):
            convert_img_to_dds(img)
            os.remove(img)
        ytd = convert_folder_to_ytd(folder)
        folder_path = Path(folder)
        output_file_path = folder_path.parent / f"{folder_path.name}.ytd"
        with open(f'{output_file_path}', 'wb') as f:
            bytes_data = ytd.Save()
            byte_array = bytearray(list(bytes_data))
            f.write(byte_array)
            self.report({'INFO'}, f"Exported {output_file_path}")
    delete_folders(FolderList, newExportPath)
    self.report(
        {'INFO'}, f"Exported {len(FolderList)} texture dictionaries")