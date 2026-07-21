import bpy
from ..itd.operators import (
    ITDLIST_OT_add,
    ITDLIST_OT_add_to_itd,
    MESHLIST_OT_delete_mesh,
    VT_OT_export_packages_as_folders,
    VT_OT_export_packages_as_itds,
    ITDLIST_OT_assign_itd_field_from_list,
    ITDLIST_OT_remove,
    ITDLIST_OT_select_mesh_parent_from_itd,
    ITDLIST_OT_select_meshes_parent_from_itd,
)
from ..vicho_preferences import get_addon_preferences
from ..icons_load import get_icon


class ITDLIST_UL_list(bpy.types.UIList):
    bl_idname = "ITDLIST_UL_list"

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row: bpy.types.UILayout = layout.row(align=True)
            row.prop(
                item,
                "selected",
                text="",
                emboss=False,
                icon="CHECKBOX_HLT" if item.selected else "CHECKBOX_DEHLT",
            )
            row.prop(item, "name", text="", emboss=False, icon="RENDERLAYERS")
            row = layout.row(align=True)
            row.scale_x = 1.0
            row.prop(item, "game_target", text="", emboss=False, icon="MATSHADERBALL")


class MESHLIST_UL_list(bpy.types.UIList):
    bl_idname = "MESHLIST_UL_list"

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            if len(context.scene.itd_list) != 0:
                row: bpy.types.UILayout = layout.row(align=True)
                if item is not None and item.mesh is not None:
                    row.label(text=item.mesh.name, icon="FILE_3D")


class TextureTools_PT_Panel(bpy.types.Panel):
    bl_label = "Textures"
    bl_idname = "VICHOTOOLS_PT_Texture"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vicho's Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text="", icon_value=get_icon("texture_box"))

    def draw(self, context):
        preferences = get_addon_preferences()
        layout = self.layout
        scene = context.scene
        resize_dds = preferences.resize_dds 

        selected_itd = scene.itd_list[scene.itd_active_index] if len(scene.itd_list) > 0 else None
        header, panel = layout.panel("package_tools", default_closed=False)
        header.label(text="Create Package(s)", icon_value=get_icon("package"))
        if panel:
            row = panel.row()
            col = row.column(align=True)
            col.operator(ITDLIST_OT_add.bl_idname, text="", icon_value=get_icon("package_variant_plus"))
            col.operator(ITDLIST_OT_remove.bl_idname, text="", icon_value=get_icon("package_variant_minus"))
            col.separator()
            col.operator(ITDLIST_OT_add_to_itd.bl_idname, text="", icon_value=get_icon("inbox_arrow_down"))
            col.separator()
            col.operator(
                ITDLIST_OT_assign_itd_field_from_list.bl_idname,
                text="",
                icon_value=get_icon("auto_fix"),
            )
            row = row.row()
            col = row.column(align=True)
            col.template_list(
                ITDLIST_UL_list.bl_idname, "", scene, "itd_list", scene, "itd_active_index"
            )
            row = row.row()
            col = row.column(align=True)
            col.template_list(
                MESHLIST_UL_list.bl_idname, "", scene, "mesh_list", scene, "mesh_active_index"
            )
            row = row.row()
            col = row.column(align=True)
            col.operator(
                ITDLIST_OT_select_meshes_parent_from_itd.bl_idname,
                text="",
                icon="ZOOM_ALL",
            )
            col.operator(
                ITDLIST_OT_select_mesh_parent_from_itd.bl_idname,
                text="",
                icon="ZOOM_SELECTED",
            )
            col.separator()
            col.operator(MESHLIST_OT_delete_mesh.bl_idname, text="", icon="X")
            if selected_itd is not None:
                col = layout.column(align=True)
                menu_flow = col.grid_flow(row_major=True, columns=3, even_columns=True, even_rows=True, align=True)
                menu_flow.prop(scene, "itd_menu", expand=True)
                box = col.box()
                col_box = box.column(align=True)
                match scene.itd_menu:
                    case "SETTINGS":
                        col_box.separator()
                        resize_dds_label = "disabled" if not resize_dds else "enabled"
                        col_box.label(text=f"DDS resizing is globally {resize_dds_label}.", icon="INFO")
                        col_box.separator()
                        col_box.prop(selected_itd, "max_pixel_size", text="Max Pixel Size", icon_value=get_icon("image_size_select_large"))
                        col_box.separator()
                        col_box.prop(selected_itd, "dds_conv_quality", text="Quality", icon_value=get_icon("image_auto_adjust"))
                        col_box.separator()
                    case "EXPORT":
                        col_box.separator()
                        col_box.prop(scene, "itd_export_path", text="", icon_value=get_icon("folder_arrow_right"))
                        col_box.prop(scene, "itd_show_explorer_after_export", text="Show Explorer After Export", icon_value=get_icon("open_in_new"))
                        col_box.separator()
                        row_box = col_box.row(align=True)
                        row_box.prop(scene, "itd_enum_process_type", text="", icon_value=get_icon("list_status"))
                        row_box.label(text="", icon_value=get_icon("arrow_right_bold"))
                        row_box.operator(VT_OT_export_packages_as_itds.bl_idname, text="Export ITDs", icon_value=get_icon("folder_multiple_image"))
                        if preferences.enable_folder_export:
                            row_box.operator(VT_OT_export_packages_as_folders.bl_idname, text="Export Folder(s)", icon_value=get_icon("folder_multiple_image"))
                        col_box.separator()