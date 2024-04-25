import os
from pathlib import Path
import shutil
import bpy

from .cw_py.cw_py_misc import get_folder_list_from_dir, get_non_dds
from ..vicho_dependencies import depen_installed

if depen_installed():
    from .cw_py.cw_ytd_tools import convert_folder_to_ytd, convert_img_to_dds


def create_ytd_folders(FolderList, ExportPath):
    for folder in FolderList:
        folder_path = os.path.join(ExportPath, folder.name)
        print(f'Added folder {folder_path}')
        os.makedirs(folder_path, exist_ok=True)
        for img in folder.image_list:
            shutil.copy(str(img.filepath), folder_path)


def delete_folders(FolderList, ExportPath):
    for folder in FolderList:
        folder_path = os.path.join(ExportPath, folder.name)
        shutil.rmtree(folder_path)


def image_paths_from_objects(objs):
    image_paths = []
    for obj in objs:
        for slot in obj.mesh.material_slots:
            if slot.material:
                for node in slot.material.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        bpy.ops.file.make_paths_absolute()
                        if not node.image or not node.image.filepath:
                            continue
                        image_paths.append(node.image.filepath)
    return image_paths


def mesh_list_from_objects(objects):
    new_mesh_list = []
    for obj in objects:
        if obj.type == 'MESH' or obj.sollum_type == 'sollumz_drawable_model':
            new_mesh_list.append(obj)
        elif obj.sollum_type == 'sollumz_drawable':
            if obj.children:
                for child in obj.children:
                    if child.sollum_type == 'sollumz_drawable_model':
                        new_mesh_list.append(child)
        elif obj.sollum_type == 'sollumz_drawable_dictionary':
            if obj.children:
                for draw_child in obj.children:
                    if draw_child.sollum_type == 'sollumz_drawable':
                        if draw_child.children:
                            for model_child in draw_child.children:
                                if model_child.type == 'MESH' or model_child.sollum_type == 'sollumz_drawable_model':
                                    new_mesh_list.append(model_child)
        elif obj.sollum_type == 'sollumz_fragment':
            if obj.children:
                for draw_child in obj.children:
                    if draw_child.sollum_type == 'sollumz_drawable':
                        if draw_child.children:
                            for model_child in draw_child.children:
                                if model_child.type == 'MESH' or model_child.sollum_type == 'sollumz_drawable_model':
                                    new_mesh_list.append(model_child)
    return new_mesh_list


def add_ytd_to_list(scene, objs, ytd_list, self=None):

    objects = mesh_list_from_objects(objs)

    if not mesh_exist_in_ytd(scene, objects, self):
        item = scene.ytd_list.add()
        item.name = f"TextureDictionary{len(ytd_list)}"
        for obj in objects:
            item.mesh_list.add().mesh = obj
            self.report({'INFO'}, f"Added {obj.name} to {item.name}")
        for image_path in image_paths_from_objects(item.mesh_list):
            item.image_list.add().filepath = image_path
        return True


def reload_images_from_ytd_list(ytd_list, self=None):
    bpy.ops.file.make_paths_absolute()
    for ytd in ytd_list:
        ytd.image_list.clear()
        for mesh in ytd.mesh_list:
            for slot in mesh.mesh.material_slots:
                if slot.material:
                    for node in slot.material.node_tree.nodes:
                        if node.type == 'TEX_IMAGE':
                            if not node.image or not node.image.filepath:
                                continue
                            ytd.image_list.add().filepath = node.image.filepath
        self.report({'INFO'}, f"Reloaded all textures in {ytd.name}")


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
    for ytyp in scene.ytyps:
        for arch in ytyp.archetypes:
            if arch.type == 'sollumz_archetype_base' or arch.type == 'sollumz_archetype_time':
                for ytd in scene.ytd_list:
                    for m in ytd.mesh_list:
                        if m.mesh.sollum_type == 'sollumz_drawable_model' and m.mesh.parent.sollum_type == 'sollumz_drawable':
                            if m.mesh.parent.name == arch.asset_name:
                                arch.texture_dictionary = ytd.name
                                self.report(
                                    {'INFO'}, f"Assigned {ytd.name} to {arch.asset_name}")


if depen_installed():
    def export_ytd_files(FolderList, ExportPath, self, scene):
        print(f'Export path: {ExportPath}')
        newExportPath = os.path.join(ExportPath, 'output')
        create_ytd_folders(FolderList, newExportPath)
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
                self.report({'INFO'}, f"Exported {output_file_path}.ytd")

        delete_folders(FolderList, newExportPath)

        self.report(
            {'INFO'}, f"Exported {len(FolderList)} texture dictionaries")