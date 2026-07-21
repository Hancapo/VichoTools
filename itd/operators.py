import os
import subprocess
import time

import bpy

from ..shared.constants import YTD_SOLLUM_TYPES
from ..shared.helper import abs_path
from ..vicho_preferences import get_addon_preferences as prefs
from .helper import (
    add_itd_to_list,
    add_meshes_to_itd,
    auto_fill_ytd_field,
    export_img_folders,
    export_img_packages,
)


class VT_OT_export_packages_as_folders(bpy.types.Operator):
    """Export the list of texture package(s) as folder(s)"""

    bl_idname = "textures.exportpkgsasfolders"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return len(context.scene.itd_list) > 0 and os.path.exists(
            abs_path(context.scene.itd_export_path)
        )

    def execute(self, context):
        start = time.time()
        scene = context.scene
        export_mode = scene.itd_enum_process_type
        ytds = []
        match export_mode:
            case "ALL":
                ytds = scene.itd_list
            case "CHECKED":
                ytds = [ytd for ytd in scene.itd_list if ytd.selected]
            case "SELECTED":
                ytds = [scene.itd_list[scene.itd_active_index]]
        output_folder = export_img_folders(ytds, abs_path(scene.itd_export_path), self)
        if scene.itd_show_explorer_after_export:
            print(f"Opening in explorer: {scene.itd_export_path}")
            subprocess.Popen(
                'explorer "{}"'.format(
                    os.path.join(scene.itd_export_path, output_folder)
                )
            )
        self.report(
            {"INFO"},
            f"Exported {len(ytds)} folder(s) in {round(time.time() - start, 4)} seconds",
        )
        return {"FINISHED"}


class VT_OT_export_packages_as_itds(bpy.types.Operator):
    """Export the list of texture package(s) as ITD file(s)"""

    bl_idname = "textures.exportpkgsasitd"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return len(context.scene.itd_list) > 0 and os.path.exists(
            bpy.path.abspath(context.scene.itd_export_path)
        )

    def execute(self, context):
        start = time.time()
        scene = context.scene
        itd_list = scene.itd_list
        export_mode = scene.itd_enum_process_type
        resize_dds: bool = prefs().resize_dds
        output_folder: str = abs_path(scene.itd_export_path)
        itds = []
        match export_mode:
            case "ALL":
                itds = itd_list
            case "CHECKED":
                itds = [itd for itd in itd_list if itd.selected]
            case "ACTIVE":
                itds = [itd_list[scene.itd_active_index]]

        export_img_packages(
            itds,
            output_folder,
            resize_dds,
            self,
        )
        if scene.itd_show_explorer_after_export:
            subprocess.Popen('explorer "{}"'.format(output_folder))
        self.report(
            {"INFO"},
            f"Exported {len(itds)} YTD(s) in {round(time.time() - start, 4)} seconds",
        )
        return {"FINISHED"}


class ITDLIST_OT_add(bpy.types.Operator):
    """Creates a new texture package from the selected object(s)"""

    bl_idname = "itd_list.add_itd"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        is_compatible_type_selected = all(
            obj.sollum_type in YTD_SOLLUM_TYPES for obj in context.selected_objects
        )
        include_mesh_objects = prefs().add_nonsollumz_to_ytd and all(
            obj.type == "MESH" for obj in context.selected_objects
        )
        return context.selected_objects and (
            is_compatible_type_selected or include_mesh_objects
        )

    def execute(self, context):
        scene = context.scene
        ytd_list = scene.itd_list
        sel_objs = context.selected_objects
        if not (add_itd_to_list(scene, sel_objs, ytd_list, self)):
            self.report({"ERROR"}, "Failed to add a new texture dictionary")
        else:
            scene.itd_active_index = len(ytd_list) - 1
        return {"FINISHED"}


class ITDLIST_OT_remove(bpy.types.Operator):
    """Removes the selected texture package from the list"""

    bl_idname = "itd_list.remove_itd"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return context.scene.itd_active_index >= 0 and len(context.scene.itd_list) > 0

    def execute(self, context):
        scene = context.scene
        list = scene.itd_list
        index = scene.itd_active_index

        list.remove(index)

        if index > 0:
            index = index - 1

        scene.itd_active_index = index
        if len(list) == 0:
            scene.mesh_list.clear()
        return {"FINISHED"}


class ITDLIST_OT_add_to_itd(bpy.types.Operator):
    """Add selected objects to the selected texture package"""

    bl_idname = "itd_list.add_to_itd"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return context.scene.itd_active_index >= 0 and len(context.scene.itd_list) > 0

    def execute(self, context):
        scene = context.scene
        selec_objs = context.selected_objects
        if add_meshes_to_itd(scene.itd_active_index, selec_objs, scene, self):
            self.report(
                {"INFO"},
                f"Added selected objects to {scene.itd_list[scene.itd_active_index].name}",
            )
        scene.mesh_list.clear()
        scene.itd_active_index = scene.itd_active_index
        return {"FINISHED"}


class ITDLIST_OT_assign_itd_field_from_list(bpy.types.Operator):
    """Auto-fill Texture Dictionary field in all YTYPs"""

    bl_idname = "itd_list.assign_itd_field_from_list"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return (
            context.scene.itd_active_index >= 0
            and len(context.scene.itd_list) > 0
            and len(context.scene.ytyps) > 0
        )

    def execute(self, context):
        scene = context.scene
        auto_fill_ytd_field(scene, self)
        return {"FINISHED"}


class ITDLIST_OT_select_meshes_parent_from_itd(bpy.types.Operator):
    """Select meshes' parent from the selected texture package"""

    bl_idname = "itd_list.select_meshes_parent_from_itd_folder"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return context.scene.itd_active_index >= 0 and len(context.scene.itd_list) > 0

    def execute(self, context):
        scene = context.scene
        list = scene.itd_list
        index = scene.itd_active_index
        mesh_list = [mesh.mesh for mesh in list[index].mesh_list]
        for mesh in mesh_list:
            if mesh.parent and mesh.parent.sollum_type != "sollum_none":
                mesh.parent.select_set(True)
                continue
            mesh.select_set(True)

        return {"FINISHED"}


class ITDLIST_OT_select_mesh_parent_from_itd(bpy.types.Operator):
    """Select mesh' parent from the selected mesh item"""

    bl_idname = "itd_list.select_mesh_parent_from_itd_folder"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return context.scene.itd_active_index >= 0 and len(context.scene.itd_list) > 0

    def execute(self, context):
        scene = context.scene
        list = scene.itd_list
        index = scene.itd_active_index
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
        ytd_list = scene.itd_list
        mesh_active_index = scene.mesh_active_index
        ytd_active_index = scene.itd_active_index

        mesh_list.remove(mesh_active_index)
        ytd_list[ytd_active_index].mesh_list.remove(mesh_active_index)

        if len(ytd_list[ytd_active_index].mesh_list) < 1:
            ytd_list.remove(ytd_active_index)
            # select any available texture dictionary
            if len(ytd_list) > 0:
                scene.itd_active_index = max(0, ytd_active_index - 1)

        scene.mesh_active_index = max(0, mesh_active_index - 1)
        return {"FINISHED"}

    def invoke(self, context, event):
        if len(context.scene.itd_list[context.scene.itd_active_index].mesh_list) == 1:
            return bpy.ops.mesh_list.confirm_delete_mesh("INVOKE_DEFAULT")
        else:
            return self.execute(context)
