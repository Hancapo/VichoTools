import bpy
from .vicho_operators import (VICHO_OT_mlo_ymap_file_browser, 
                              VICHO_OT_paste_obj_trans_from_pick_obj, 
                              VICHO_OT_del_all_cols_attrs, 
                              VICHO_OT_del_all_vgs, 
                              VICHO_OT_detect_meshes_no_textures, 
                              VICHO_OT_rename_all_uvs,
                              VICHO_OT_rename_all_cas)

class VichoMloTools_PT_Panel(bpy.types.Panel):
    bl_label = "MLO"
    bl_idname = "VICHOTOOLS_PT_Mlo"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vicho's Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text="", icon="HOME")

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "ymap_instance_name_field", text="Instance name")
        row = layout.row()
        row.operator(VICHO_OT_mlo_ymap_file_browser.bl_idname)


class VichoObjectTools_PT_Panel(bpy.types.Panel):
    bl_label = "Objects"
    bl_idname = "VICHOTOOLS_PT_Object"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vicho's Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text="", icon="OVERLAY")

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        row = col.row(align=True)
        col = row.column(align=True)
        col.prop(context.scene, "PasteDataToObject", text="From")
        col.prop(context.scene, "CopyDataFromObject", text="To")
        col.separator()
        row = col.row(align=True)
        row.prop(context.scene, "locationOb_checkbox", text="Location",icon="ORIENTATION_VIEW")
        row.prop(context.scene, "rotationOb_checkbox", text="Rotation", icon="ORIENTATION_GIMBAL")
        row.prop(context.scene, "scaleOb_checkbox", text="Scale", icon="OBJECT_ORIGIN")

        col.operator(VICHO_OT_paste_obj_trans_from_pick_obj.bl_idname, icon="MOD_SIMPLIFY")

        # Section 3: Delete Meshes Without Data
        col.separator()
        col.label(text="Delete", icon="TRASH")
        col.separator()
        # Section 4: Delete All Color Attributes
        col.operator(VICHO_OT_del_all_cols_attrs.bl_idname, icon="COLOR")
        # Section 5: Delete All Vertex Groups
        col.operator(VICHO_OT_del_all_vgs.bl_idname, icon="GROUP_VERTEX")
        col.separator()

        col.label(text="Misc", icon="MESH_GRID")
        col.separator()
        col.operator(VICHO_OT_detect_meshes_no_textures.bl_idname)
        col.separator()

        col.label(text="Rename", icon="GREASEPENCIL")
        col.separator()
        col.operator(VICHO_OT_rename_all_uvs.bl_idname, icon="UV_DATA")
        col.operator(VICHO_OT_rename_all_cas.bl_idname, icon="COLOR")
        col.separator()
