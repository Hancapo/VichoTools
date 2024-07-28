import os
import subprocess
import bpy

from ..vicho_preferences import get_addon_preferences
from ..vicho_dependencies import dependencies_manager as d

from .funcs import export_ytd_files

from .funcs import (
    add_meshes_to_ytd,
    add_ytd_to_list,
    auto_fill_ytd_field,
    create_ytd_folders,
)


class ExportYTDFolders(bpy.types.Operator):
    """Export the list of texture folders as folders"""

    bl_idname = "vicho.exportytdfolders"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return len(context.scene.ytd_list) > 0 and os.path.exists(
            bpy.path.abspath(context.scene.ytd_export_path)
        )

    def execute(self, context):
        if not d.available:
            return {"CANCELLED"}
        scene = context.scene
        export_mode = scene.ytd_enum_process_type
        ytds = []
        match export_mode:
            case "ALL":
                ytds = scene.ytd_list
            case "CHECKED":
                ytds = [ytd for ytd in scene.ytd_list if ytd.selected]
            case "SELECTED":
                ytds = [scene.ytd_list[scene.ytd_active_index]]
        create_ytd_folders(ytds, bpy.path.abspath(scene.ytd_export_path), self)
        if scene.ytd_show_explorer_after_export:
            subprocess.Popen(
                'explorer "{}"'.format(bpy.path.abspath(scene.ytd_export_path))
            )
        return {"FINISHED"}


class ExportYTDFiles(bpy.types.Operator):
    """Export the list of texture folders as YTD files"""

    bl_idname = "vicho.exportytdfiles"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return len(context.scene.ytd_list) > 0 and os.path.exists(
            bpy.path.abspath(context.scene.ytd_export_path)
        )

    def execute(self, context):
        if not d.available:
            return {"CANCELLED"}
        scene = context.scene
        export_mode = scene.ytd_enum_process_type
        ytds = []
        match export_mode:
            case "ALL":
                ytds = scene.ytd_list
            case "CHECKED":
                ytds = [ytd for ytd in scene.ytd_list if ytd.selected]
            case "SELECTED":
                ytds = [scene.ytd_list[scene.ytd_active_index]]

        export_ytd_files(ytds, bpy.path.abspath(scene.ytd_export_path), self)
        if scene.ytd_show_explorer_after_export:
            subprocess.Popen(
                'explorer "{}"'.format(
                    bpy.path.abspath(scene.ytd_export_path) + "output"
                )
            )
        return {"FINISHED"}


class YTDLIST_OT_add(bpy.types.Operator):
    """Creates a new texture folder from the selected objects"""

    bl_idname = "ytd_list.add_ytd"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        preferences = get_addon_preferences()
        compatible_sollum_types = [
            "sollumz_drawable",
            "sollumz_fragment",
            "sollumz_drawable_model",
            "sollumz_drawable_dictionary",
        ]

        is_compatible_type_selected = all(
            obj.sollum_type in compatible_sollum_types
            for obj in context.selected_objects
        )
        include_mesh_objects = preferences.add_nonsollumz_to_ytd and all(
            obj.type == "MESH" for obj in context.selected_objects
        )
        return context.selected_objects and (
            is_compatible_type_selected or include_mesh_objects
        )

    def execute(self, context):
        scene = context.scene
        ytd_list = scene.ytd_list
        sel_objs = context.selected_objects
        if not (add_ytd_to_list(scene, sel_objs, ytd_list, self)):
            self.report({"ERROR"}, "Failed to add a new texture dictionary")
        else:
            scene.ytd_active_index = len(ytd_list) - 1
        return {"FINISHED"}


class YTDLIST_OT_remove(bpy.types.Operator):
    """Removes the selected texture folder from the list"""

    bl_idname = "ytd_list.remove_ytd"
    bl_label = ""

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
        if len(list) == 0:
            scene.mesh_list.clear()
        return {"FINISHED"}


class YTDLIST_OT_add_to_ytd(bpy.types.Operator):
    """Add selected objects to the selected texture folder"""

    bl_idname = "ytd_list.add_to_ytd"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return context.scene.ytd_active_index >= 0 and len(context.scene.ytd_list) > 0

    def execute(self, context):
        scene = context.scene
        selec_objs = context.selected_objects
        if add_meshes_to_ytd(scene.ytd_active_index, selec_objs, scene, self):
            self.report(
                {"INFO"},
                f"Added selected objects to {scene.ytd_list[scene.ytd_active_index].name}",
            )
        scene.mesh_list.clear()
        scene.ytd_active_index = scene.ytd_active_index
        return {"FINISHED"}


class YTDLIST_OT_assign_ytd_field_from_list(bpy.types.Operator):
    """Auto-fill Texture Dictionary field in all YTYPs"""

    bl_idname = "ytd_list.assign_ytd_field_from_list"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return (
            context.scene.ytd_active_index >= 0
            and len(context.scene.ytd_list) > 0
            and len(context.scene.ytyps) > 0
        )

    def execute(self, context):
        scene = context.scene
        auto_fill_ytd_field(scene, self)
        return {"FINISHED"}


class YTDLIST_OT_select_meshes_from_ytd_folder(bpy.types.Operator):
    """Select meshes' parent from the selected texture folder"""

    bl_idname = "ytd_list.select_meshes_from_ytd_folder"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return context.scene.ytd_active_index >= 0 and len(context.scene.ytd_list) > 0

    def execute(self, context):
        scene = context.scene
        list = scene.ytd_list
        index = scene.ytd_active_index
        mesh_list = [mesh.mesh for mesh in list[index].mesh_list]
        for mesh in mesh_list:
            if mesh.parent and mesh.parent.sollum_type != "sollum_none":
                mesh.parent.select_set(True)
                continue
            mesh.select_set(True)

        return {"FINISHED"}


class YTDLIST_OT_select_mesh_from_ytd_folder(bpy.types.Operator):
    """Select mesh' parent from the selected mesh item"""

    bl_idname = "ytd_list.select_mesh_from_ytd_folder"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return context.scene.ytd_active_index >= 0 and len(context.scene.ytd_list) > 0

    def execute(self, context):
        scene = context.scene
        list = scene.ytd_list
        index = scene.ytd_active_index
        mesh = list[index].mesh_list[scene.mesh_active_index].mesh
        if mesh.parent and mesh.parent.sollum_type != "sollum_none":
            mesh.parent.select_set(True)
        else:
            mesh.select_set(True)
        return {"FINISHED"}





class MESHLIST_OT_confirm_delete_mesh(bpy.types.Operator):
    """Confirm deletion of the last mesh from the list"""

    bl_idname = "mesh_list.confirm_delete_mesh"
    bl_label = "Are you sure you want to delete the last mesh?"

    @classmethod
    def poll(cls, context):
        return len(context.scene.mesh_list) > 0 and context.scene.mesh_active_index >= 0

    def execute(self, context):
        bpy.ops.mesh_list.delete_mesh()
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class MESHLIST_OT_delete_mesh(bpy.types.Operator):
    """Delete the selected mesh from the list"""

    bl_idname = "mesh_list.delete_mesh"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return len(context.scene.mesh_list) > 0 and context.scene.mesh_active_index >= 0

    def execute(self, context):
        scene = context.scene
        mesh_list = scene.mesh_list
        ytd_list = scene.ytd_list
        mesh_active_index = scene.mesh_active_index
        ytd_active_index = scene.ytd_active_index

        mesh_list.remove(mesh_active_index)
        ytd_list[ytd_active_index].mesh_list.remove(mesh_active_index)

        if len(ytd_list[ytd_active_index].mesh_list) < 1:
            ytd_list.remove(ytd_active_index)
            # select any available texture dictionary
            if len(ytd_list) > 0:
                scene.ytd_active_index = max(0, ytd_active_index - 1)

        scene.mesh_active_index = max(0, mesh_active_index - 1)
        return {"FINISHED"}

    def invoke(self, context, event):
        if len(context.scene.ytd_list[context.scene.ytd_active_index].mesh_list) == 1:
            return bpy.ops.mesh_list.confirm_delete_mesh("INVOKE_DEFAULT")
        else:
            return self.execute(context)
