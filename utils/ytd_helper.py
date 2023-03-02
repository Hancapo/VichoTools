import bpy
import os
import shutil


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


class YTDLIST_OT_add(bpy.types.Operator):
    """Add a new texture dictionary to the list"""
    bl_idname = "ytd_list.add_ytd"
    bl_label = "Add a new texture dictionary"

    @classmethod
    def poll(cls, context):
        return context.scene.objects is not None and (context.selected_objects and
                                                      all(obj.type == 'MESH' for obj in context.selected_objects))

    def execute(self, context):
        scene = context.scene
        ytd_list = scene.ytd_list
        sel_objs = context.selected_objects
        if not (add_ytd_to_list(scene, sel_objs, ytd_list, self)):
            self.report({'ERROR'}, f"Failed to add a new texture dictionary")
        return {'FINISHED'}


class YTDLIST_OT_remove(bpy.types.Operator):
    """Remove the selected texture dictionary from the list"""
    bl_idname = "ytd_list.remove_ytd"
    bl_label = "Remove the selected texture dictionary"

    @classmethod
    def poll(cls, context):
        return context.scene.ytd_active_index >= 0 and len(context.scene.ytd_list) > 0

    def execute(self, context):
        scene = context.scene
        list = scene.ytd_list
        index = scene.ytd_active_index

        list.remove(index)

        if index > 0:
            index = index - 1

        scene.ytd_active_index = index
        return {'FINISHED'}


class YTDLIST_OT_reload_all(bpy.types.Operator):
    """Reload all texture dictionaries from the list to include changes made to the textures"""
    bl_idname = "ytd_list.reload_all"
    bl_label = "Reload all texture dictionaries"

    @classmethod
    def poll(cls, context):
        return context.scene.ytd_active_index >= 0 and len(context.scene.ytd_list) > 0

    def execute(self, context):
        scene = context.scene
        list = scene.ytd_list
        reload_images_from_ytd_list(list, self)
        return {'FINISHED'}


class YTDLIST_OT_add_to_ytd(bpy.types.Operator):
    """Add selected objects to the selected texture dictionary and reload the textures"""
    bl_idname = "ytd_list.add_to_ytd"
    bl_label = "Add selected objects to the selected texture dictionary"

    @classmethod
    def poll(cls, context):
        return context.scene.ytd_active_index >= 0 and len(context.scene.ytd_list) > 0

    def execute(self, context):
        scene = context.scene
        selec_objs = context.selected_objects
        if add_meshes_to_ytd(scene.ytd_active_index, selec_objs, scene, self):
            reload_images_from_ytd_list(scene.ytd_list, self)
            self.report(
                {'INFO'}, f"Added selected objects to {scene.ytd_list[scene.ytd_active_index].name}")
        return {'FINISHED'}

class YTDLIST_OT_assign_ytd_field_from_list(bpy.types.Operator):
    """Auto-fill Texture Dictionary field in all YTYPs"""
    bl_idname = "ytd_list.assign_ytd_field_from_list"
    bl_label = "Auto-fill Texture Dictionary field"

    @classmethod
    def poll(cls, context):
        return context.scene.ytd_active_index >= 0 and len(context.scene.ytd_list) > 0

    def execute(self, context):
        scene = context.scene
        auto_fill_ytd_field(scene, self)
        return {'FINISHED'}

def ExportYTDFolders(FolderList, ExportPath):
    for folder in FolderList:
        folder_path = os.path.join(ExportPath, folder.name)
        os.makedirs(folder_path, exist_ok=True)
        for img in folder.image_list:
            shutil.copy(str(img.filepath), folder_path)


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
                        if m.mesh.parent.parent.name == arch.asset_name or m.mesh.name == arch.asset_name:
                            arch.texture_dictionary = ytd.name
                            self.report({'INFO'}, f"Assigned {ytd.name} to {arch.asset_name}")