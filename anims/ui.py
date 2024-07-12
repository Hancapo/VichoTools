import bpy

class VichoAnimsToolsPanel(bpy.types.Panel):
    bl_label = "Anims"
    bl_idname = "VichoAnimsTools_PT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Tools"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text="", icon="RENDER_ANIMATION")

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.separator()
        col.operator("anim.create_anims_from_selected", text="Create YCD from Selected Objects", icon="UV")
        col.separator()
        col.prop(context.scene, "ycd_name", text="YCD Name", icon='ANIM')
        col.separator()
        row = col.row(align=True)
        row.separator()
        row.prop(context.scene, "autofill_clipdict", text="Autofill Clip Dictionary", icon='GREASEPENCIL')
        row.prop(context.scene, "calculate_anim_flags", text="Calculate Anim Flags", icon='EXPERIMENTAL')
        row.prop(context.scene, "auto_start_anim_flag", text="Auto-start Anim", icon='SOLO_ON')