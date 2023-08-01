import bpy
from ..ui import VichoFragmentToolsPanel


class Vicho_FragmentGlassWindowsPanel(bpy.types.Panel):
    bl_label = "Glass Windows Tools"
    bl_idname = "VICHO_PT_glass_windows_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Misc Tools"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = VichoFragmentToolsPanel.bl_idname

    def draw_header(self, context):
        self.layout.label(text="", icon="MOD_BUILD")

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        list_col = row.column()
        scene = context.scene
        list_col.template_list("GlassFragList", "", scene,
                               "glass_frag_list", scene, "glass_frag_active_index")
        list_col2 = row.column(align=True)
        list_col2.operator("glass_frag_list.add_glass", icon="ADD", text="")
        list_col2.operator("glass_frag_list.remove_glass",
                           icon="REMOVE", text="")
        list_col.separator()
        list_col.operator("glass_frag_list.export_xml",
                          icon="EXPORT", text="Export to XML")
        list_col.separator()
        active_index = scene.glass_frag_active_index
        if 0 <= active_index < len(scene.glass_frag_list):

            glass_item = scene.glass_frag_list[active_index]
            layout.label(text="Glass Window Properties",
                         icon="MOD_TRIANGULATE")
            col3 = layout.column(align=True)
            col3.prop(glass_item, "flags")
            col3.prop(glass_item, "unk_float_13")
            col3.prop(glass_item, "unk_float_14")

            col4 = layout.column(align=True)
            col4.prop(glass_item, "unk_float_15")
            col4.prop(glass_item, "unk_float_16")
            col4.prop(glass_item, "thickness")

            col5 = layout.column(align=True)
            col5.prop(glass_item, "unk_float_18")
            col5.prop(glass_item, "unk_float_19")
            col5.prop(glass_item, "layout_type")
