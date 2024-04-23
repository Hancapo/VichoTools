import bpy
from .ytd.ytd_helper import *
from .vicho_properties import *
from .vicho_operators import *


class VICHO_PT_MISC1_PANEL(bpy.types.Panel):
    bl_label = "Misc Tools"
    bl_idname = "MAINMISCTOOLS_PT_"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Misc Tools"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text="", icon="ALIGN_RIGHT")

    def draw(self, context):
        layout = self.layout
        # Create category
        row = layout.row()
        row.label(
            text="Save selected object(s) as unique list to file:", icon='ALIGN_RIGHT')
        row = layout.row()
        row.prop(context.scene, "file_name_field", text="File name")
        row = layout.row()
        row.operator("vicho.selobjsastext")
        row = layout.row()


class VichoMloToolsPanel(bpy.types.Panel):
    bl_label = "MLO Tools"
    bl_idname = "VICMLOTOOLS_PT_"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Misc Tools"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text="", icon="WORLD")

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "ymap_instance_name_field",
                 text="Instance name")
        row = layout.row()
        row.operator("vicho.mloyampfilebrowser")


class VichoObjectToolsPanel(bpy.types.Panel):
    bl_label = "Object Tools"
    bl_idname = "VICHOBJECTTOOLS_PT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Misc Tools"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text="", icon="OVERLAY")

    def draw(self, context):
        layout = self.layout

        # Section 1: Reset Object Transform
        col = layout.column(align=True)
        col.label(text="Reset Object(s) Transform:", icon='PLAY_REVERSE')

        row = col.row(align=True)
        row.prop(context.scene, "location_checkbox", text="Location")
        row.prop(context.scene, "rotation_checkbox", text="Rotation")
        row.prop(context.scene, "scale_checkbox", text="Scale")

        col.operator("vicho.resetobjtransrot")

        # Section 2: Set Object Transforms to Picked Object
        col.separator()
        col.label(text="Set Object Transforms to Picked Object", icon='TRACKING_BACKWARDS')

        row = col.row(align=True)
        row.prop(context.scene, "PasteDataToObject", text="From")
        row.prop(context.scene, "CopyDataFromObject", text="To")

        row = col.row(align=True)
        row.prop(context.scene, "locationOb_checkbox", text="Location")
        row.prop(context.scene, "rotationOb_checkbox", text="Rotation")
        row.prop(context.scene, "scaleOb_checkbox", text="Scale")

        col.operator("vicho.pasteobjtransfrompickedobject")

        # Section 3: Delete Meshes Without Data
        col.separator()
        col.label(text="Delete Meshes Without Data and Others", icon='DOT')
        col.separator()

        col.operator("vicho.deleteemptyobj")
        col.separator()

        # Section 4: Delete All Color Attributes
        col.operator("vicho.deleteallcolorattributes")
        col.separator()

        # Section 5: Delete All Vertex Groups
        col.operator("vicho.deleteallvertexgroups")
        col.separator()

        col.operator("vicho.detectmesheswithnotextures")
        col.separator()

        col.operator("vicho.renamealluvmaps")
        col.separator()
        


