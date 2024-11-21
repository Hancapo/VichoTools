import bpy

from ..vicho_preferences import get_addon_preferences
from ..vicho_dependencies import dependencies_manager as d
from ..ytd.operators import (
    YTDLIST_OT_add,
    YTDLIST_OT_remove,
    YTDLIST_OT_add_to_ytd,
    YTDLIST_OT_assign_ytd_field_from_list,
    YTDLIST_OT_select_mesh_parent_from_ytd_folder,
    YTDLIST_OT_select_meshes_parent_from_ytd_folder,
)
from ..ytd.operators import MESHLIST_OT_delete_mesh, VICHO_OT_export_pkgs_as_ytds, VICHO_OT_export_pkgs_as_folders

class YTDLIST_UL_list(bpy.types.UIList):
    bl_idname = "YTDLIST_UL_list"

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.row(align=True)
            row.prop(
                item,
                "selected",
                text="",
                emboss=False,
                icon="CHECKBOX_HLT" if item.selected else "CHECKBOX_DEHLT",
            )
            row.prop(item, "name", text="", emboss=False, icon="RENDERLAYERS")
            row = layout.row(align=True)
            row.scale_x = 0.7
            row.prop(item, "game_target", text="", emboss=False, icon="MATSHADERBALL")


class MESHLIST_UL_list(bpy.types.UIList):
    bl_idname = "MESHLIST_UL_list"

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            if len(context.scene.ytd_list) != 0:
                row = layout.row(align=True)
                if item is not None and item.mesh is not None:
                    row.prop(item.mesh, "name", text="", emboss=False, icon="FILE_3D")

class TextureTools_PT_Panel(bpy.types.Panel):
    bl_label = "Textures"
    bl_idname = "VICHOTOOLS_PT_Texture"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vicho's Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text="", icon="NODE_TEXTURE")

    def draw(self, context):
        preferences = get_addon_preferences()
        layout = self.layout
        scene = context.scene
        export_available = len(scene.ytd_list) > 0 and any([item.selected for item in scene.ytd_list])

        if d.available:
            am = scene.ytd_advanced_mode
            dts = scene.divide_textures_size
            mps = scene.max_pixel_size
            row = layout.row()
            col = row.column(align=True)
            col.separator(factor=3.5)
            col.operator(YTDLIST_OT_add.bl_idname, text="", icon="ADD")
            col.operator(YTDLIST_OT_remove.bl_idname, text="", icon="REMOVE")
            col.separator()
            col.operator(YTDLIST_OT_add_to_ytd.bl_idname, text="", icon="TRANSFORM_ORIGINS")
            col.separator()
            col.operator(
                YTDLIST_OT_assign_ytd_field_from_list.bl_idname,
                text="",
                icon="CURRENT_FILE",
            )
            row = row.row()
            col = row.column(align=True)
            col.label(text="Texture Packages", icon="TEXTURE")
            col.template_list(
                YTDLIST_UL_list.bl_idname, "", scene, "ytd_list", scene, "ytd_active_index"
            )
            row = row.row()
            col = row.column(align=True)
            col.label(text="Meshes", icon="MESH_DATA")
            col.template_list(
                MESHLIST_UL_list.bl_idname, "", scene, "mesh_list", scene, "mesh_active_index"
            )
            row = row.row()
            col = row.column(align=True)
            col.separator(factor=3.5)
            col.operator(
                YTDLIST_OT_select_meshes_parent_from_ytd_folder.bl_idname,
                text="",
                icon="ZOOM_ALL",
            )
            col.operator(
                YTDLIST_OT_select_mesh_parent_from_ytd_folder.bl_idname,
                text="",
                icon="ZOOM_SELECTED",
            )
            col.separator()
            col.operator(MESHLIST_OT_delete_mesh.bl_idname, text="", icon="X")

            col = layout.column(align=True)
            col.separator()
            if export_available:
                col.label(text="Export Options", icon="EXPORT")
                box = col.box()
                col = box.column(align=True)
                row = box.row()
                col.separator()
                col.prop(scene, "ytd_advanced_mode", icon="DOWNARROW_HLT" if scene.ytd_advanced_mode else "RIGHTARROW")
                if am:
                    box2 = col.box()
                    col2 = box2.column(align=True)
                    col2.label(text="Resizing Settings", icon="IMAGE")
                    col2.separator()
                    col2.prop(scene, "divide_textures_size", text="Disable Half Texture Size" if dts else "Enable Half Texture Size", icon="IMAGE_REFERENCE" if dts else "IMAGE_PLANE")
                    col2.separator()
                    col2.prop(scene, "max_pixel_size", text="Disable Limit to" if mps else "Enable Limit to" ,icon="MODIFIER_ON" if mps else "MODIFIER_OFF" )
                    col2.prop(scene, "max_pixel_size_list", text="", icon="IMAGE_DATA")
                row.prop(scene, "dds_conv_quality", text="Quality", icon="MODIFIER")
                row = box.row()
                row.prop(scene, "ytd_export_path", text="", icon="FOLDER_REDIRECT")
                row.prop(
                    scene,
                    "ytd_show_explorer_after_export",
                    text="Show containing folder after export",
                )
                row = box.row()
                col.separator()
                col = box.column(align=True)
                col.prop(scene, "ytd_enum_process_type", text="Item(s) to export", icon="PRESET")
                row.label(text="Export as:", icon="WORKSPACE")  
                row.operator(
                    VICHO_OT_export_pkgs_as_ytds.bl_idname, text="YTD File(s)", icon="FORCE_TEXTURE"
                )
                if preferences.enable_folder_export:
                    row.operator(
                        VICHO_OT_export_pkgs_as_folders.bl_idname, text="Folder(s)", icon="FILE_FOLDER"
                    )
                col.separator()
                
        else:
            layout.label(
                text="PythonNET or .NET 8 runtime aren't installed, please make sure you check the Add-on's preference menu",
                icon="ERROR",
            )
