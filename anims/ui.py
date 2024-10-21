import bpy

from .operators import CreateClipDictionaryFromSelected


class VichoAnimTools_PT_Panel(bpy.types.Panel):
    bl_label = "Anims"
    bl_idname = "VICHOTOOLS_PT_Anim"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vicho's Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text="", icon="RENDER_ANIMATION")

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        ycd_name = context.scene.ycd_name
        col.label(
            text="This tool is experimental, it currently supports Object(s) and UV Anims.",
            icon="ERROR",
        )
        col.separator()
        col.prop(context.scene, "ycd_name", text="YCD Name", icon="ANIM")
        col.separator()
        row = col.row(align=True)
        if ycd_name != "":
            row.prop(
                context.scene,
                "autofill_clipdict",
                text="Autofill Clip Dictionary",
                icon="GREASEPENCIL",
            )
            row.prop(
                context.scene,
                "calculate_anim_flags",
                text="Calculate Anim Flags",
                icon="EXPERIMENTAL",
            )
            row.prop(
                context.scene,
                "auto_start_anim_flag",
                text="Auto-start Anim",
                icon="SOLO_ON",
            )
            col.separator()
            row = col.row(align=True)
            row.prop(context.scene.render, "fps", text="FPS")
            row = col.row(align=True)
            row.operator(
                CreateClipDictionaryFromSelected.bl_idname,
                text="Create YCD from Selected Objects",
                icon="UV",
            )
            
