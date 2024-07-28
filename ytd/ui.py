import bpy

from ..vicho_preferences import get_addon_preferences
from ..vicho_dependencies import dependencies_manager as d
from ..ytd.operators import (
    YTDLIST_OT_add,
    YTDLIST_OT_remove,
    YTDLIST_OT_add_to_ytd,
    YTDLIST_OT_assign_ytd_field_from_list,
    YTDLIST_OT_select_mesh_from_ytd_folder,
    YTDLIST_OT_select_meshes_from_ytd_folder,
)
from ..ytd.operators import MESHLIST_OT_delete_mesh, ExportYTDFiles, ExportYTDFolders
from ..ytd.helper import YTDLIST_UL_list, MESHLIST_UL_list


class VichoTextureTools_PT_Panel(bpy.types.Panel):
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
            row = layout.row()
            col = row.column(align=True)
            col.separator(factor=3.5)
            col.operator(YTDLIST_OT_add.bl_idname, text="", icon="ADD")
            col.operator(YTDLIST_OT_remove.bl_idname, text="", icon="REMOVE")
            col.separator()
            col.operator(YTDLIST_OT_add_to_ytd.bl_idname, text="", icon="IMPORT")
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
                YTDLIST_OT_select_meshes_from_ytd_folder.bl_idname,
                text="",
                icon="ZOOM_ALL",
            )
            col.operator(
                YTDLIST_OT_select_mesh_from_ytd_folder.bl_idname,
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
                    ExportYTDFiles.bl_idname, text="YTD File(s)", icon="FORCE_TEXTURE"
                )
                if preferences.enable_folder_export:
                    row.operator(
                        ExportYTDFolders.bl_idname, text="Folder(s)", icon="FILE_FOLDER"
                    )
                
        else:
            layout.label(
                text="PythonNET or .NET 8 runtime aren't installed, please make sure you check the Add-on's preference menu",
                icon="ERROR",
            )
