import subprocess
import bpy
import os
import shutil
from ..vicho_misc import get_addon_preferences


class YtdList(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()
            row.prop(item, "name", text="", emboss=False, icon='FILE_FOLDER')


class ImageString(bpy.types.PropertyGroup):
    filepath: bpy.props.StringProperty()


class MeshGroup(bpy.types.PropertyGroup):
    mesh: bpy.props.PointerProperty(type=bpy.types.Object)


class YtdItem(bpy.types.PropertyGroup):
    image_list: bpy.props.CollectionProperty(type=ImageString)
    mesh_list: bpy.props.CollectionProperty(type=MeshGroup)


def ExportYTD_Folders(FolderList, ExportPath):
    create_ytd_folders(FolderList, ExportPath)


def ExportYTD_Files(FolderList, ExportPath, self, scene):
    print(f'Export path: {ExportPath}')
    newExportPath = os.path.join(ExportPath, 'output')
    preferences = get_addon_preferences(bpy.context)
    f2ytd_path = preferences.folders2ytd_path
    folders2ytdpath = os.path.join(f2ytd_path, "Folder2YTD.exe")
    f2td_args = "-silentmode"
    if scene.mip_maps:
        f2td_args += " -mipmaps"
    f2td_args += f" -quality '{scene.quality_mode}'"
    f2td_args += f" -format '{scene.export_mode}'"
    f2td_args += f' -folder "{newExportPath}"'
    if scene.transparency:
        f2td_args += " -transparency"
    create_ytd_folders(FolderList, newExportPath)

    cmd = f'"{folders2ytdpath}" {f2td_args}'
    
    print(cmd)

    process = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print("Standard Output:")
    print(stdout.decode())
    print("Standard Error:")
    print(stderr.decode())

    while process.poll() is None:
        print("Waiting for process to finish...")
        pass
    delete_folders(FolderList, newExportPath)
    delete_ini_from_F2YTD()

    self.report(
        {'INFO'}, f"Exported {len(FolderList)} texture dictionaries")


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


def images_paths_from_objects(objs):
    image_paths = []
    for obj in objs:
        for slot in obj.material_slots:
            if slot.material:
                for node in slot.material.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        bpy.ops.file.make_paths_absolute()
                        if not node.image or not node.image.filepath:
                            continue
                        image_paths.append(node.image.filepath)
    return image_paths


def mesh_list_from_objects(objects, item):
    for obj in objects:
        if obj.type == 'MESH':
            item.mesh_list.add().mesh = obj


def add_ytd_to_list(scene, objs, ytd_list, self):
    if not mesh_exist_in_ytd(scene, objs, self):
        item = scene.ytd_list.add()
        item.name = f"TextureDictionary{len(ytd_list)}"
        for image_path in images_paths_from_objects(objs):
            item.image_list.add().filepath = image_path
        mesh_list_from_objects(objs, item)
        self.report({'INFO'}, f"Added {item.name}")
        return True


def reload_images_from_ytd_list(ytd_list, self):
    for ytd in ytd_list:
        ytd.image_list.clear()
        for mesh in ytd.mesh_list:
            for slot in mesh.mesh.material_slots:
                if slot.material:
                    for node in slot.material.node_tree.nodes:
                        if node.type == 'TEX_IMAGE':
                            bpy.ops.file.make_paths_absolute()
                            if not node.image or not node.image.filepath:
                                continue
                            ytd.image_list.add().filepath = node.image.filepath
        self.report({'INFO'}, f"Reloaded all textures in {ytd.name}")


def add_meshes_to_ytd(index: int, objects, scene, self=None):
    if not mesh_exist_in_ytd(scene, objects, self):
        for obj in objects:
            scene.ytd_list[index].mesh_list.add().mesh = obj
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
                        is_sollumz_yft = False
                        if m.mesh.sollum_type == 'sollumz_drawable_model' and m.mesh.parent.sollum_type == 'sollumz_drawable':
                            is_sollumz_yft = True
                        if is_sollumz_yft:
                            if m.mesh.parent.name == arch.asset_name:
                                arch.texture_dictionary = ytd.name
                                self.report(
                                    {'INFO'}, f"Assigned {ytd.name} to {arch.asset_name}")
                        else:
                            if m.mesh.parent.parent.name == arch.asset_name or m.mesh.name == arch.asset_name:
                                arch.texture_dictionary = ytd.name
                                self.report(
                                    {'INFO'}, f"Assigned {ytd.name} to {arch.asset_name}")


def delete_ini_from_F2YTD():
    preferences = get_addon_preferences(bpy.context)
    f2ytd_path = preferences.folders2ytd_path
    ini_path = os.path.join(f2ytd_path, "config.ini")
    if os.path.exists(ini_path):
        os.remove(ini_path)
