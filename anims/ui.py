import bpy

class VichoAnimsToolsPanel(bpy.types.Panel):
    bl_label = "Anims Tools"
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

        # Section 1: Set Object Transforms to Picked Object
        col.separator()
        col.operator("anim.create_uv_anims_from_selected", text="Create UV Animations from Selected Objects", icon="UV")
        col.separator()
        col.prop(context.scene, "ycd_name", text="YCD Name")