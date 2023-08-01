import os
import subprocess
import bpy

from ..vicho_misc import get_addon_preferences
from .ytd_helper import ExportYTD_Files, ExportYTD_Folders, add_meshes_to_ytd, add_ytd_to_list, auto_fill_ytd_field, reload_images_from_ytd_list

class ExportYTDFolders(bpy.types.Operator):
    """Export the list of texture dictionaries as folders"""
    bl_idname = "vicho.exportytdfolders"
    bl_label = "Export YTD folders"

    @classmethod
    def poll(cls, context):
        return len(context.scene.ytd_list) > 0 and os.path.exists(bpy.path.abspath(context.scene.ytd_export_path))

    def execute(self, context):
        ytds = context.scene.ytd_list
        ExportYTD_Folders(ytds, bpy.path.abspath(context.scene.ytd_export_path))
        subprocess.Popen('explorer "{}"'.format(bpy.path.abspath(context.scene.ytd_export_path)))
        return {'FINISHED'}


class ExportYTDFiles(bpy.types.Operator):
    """Export the list of texture dictionaries as YTD files"""
    bl_idname = "vicho.exportytdfiles"
    bl_label = "Export YTD files"

    @classmethod
    def poll(cls, context):
        preferences = get_addon_preferences(bpy.context)
        f2ytd_loaded: bool = os.path.isfile(preferences.folders2ytd_path + "Folder2YTD.exe") 
        return len(context.scene.ytd_list) > 0 and os.path.exists(bpy.path.abspath(context.scene.ytd_export_path)) and context.scene.convert_to_ytd and f2ytd_loaded

    def execute(self, context):
        scene = context.scene
        ytds = scene.ytd_list
        ExportYTD_Files(ytds, bpy.path.abspath(scene.ytd_export_path), self, scene)
        subprocess.Popen('explorer "{}"'.format(bpy.path.abspath(scene.ytd_export_path)))
        return {'FINISHED'}


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
        return context.scene.ytd_active_index >= 0 and len(context.scene.ytd_list) > 0 and len(context.scene.ytyps) > 0

    def execute(self, context):
        scene = context.scene
        auto_fill_ytd_field(scene, self)
        return {'FINISHED'}
