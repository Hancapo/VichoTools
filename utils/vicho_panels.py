import bpy
import os
from mathutils import Quaternion
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from .ytd_helper import *
from .vicho_funcs import *
import subprocess
from .vicho_operators import *


class VICHO_PT_MAIN_PANEL(bpy.types.Panel):
    bl_label = "Vicho's Tools"
    bl_idname = "VICHO_PT_MAIN_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vicho's Tools"

    def draw_header(self, context):
        self.layout.label(text="", icon="TOOL_SETTINGS")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True


class VICHO_PT_MISC1_PANEL(bpy.types.Panel):
    bl_label = "Misc Tools"
    bl_idname = "MAINMISCTOOLS_PT_"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Misc Tools"
    bl_parent_id = VICHO_PT_MAIN_PANEL.bl_idname
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
        row.operator("custom.selobjsastext")
        row = layout.row()


class VichoMloToolsPanel(bpy.types.Panel):
    bl_label = "MLO Tools"
    bl_idname = "VICMLOTOOLS_PT_"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Misc Tools"
    bl_parent_id = VICHO_PT_MAIN_PANEL.bl_idname
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
    bl_idname = "VICHOBJECTTOOLS_PT_"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Misc Tools"
    bl_parent_id = VICHO_PT_MAIN_PANEL.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text="", icon="OVERLAY")

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Reset Object(s) transform:", icon='PLAY_REVERSE')
        row = layout.row()
        row.prop(context.scene, "location_checkbox", text="Reset Location")
        row.prop(context.scene, "rotation_checkbox", text="Reset Rotation")
        row.prop(context.scene, "scale_checkbox", text="Reset Scale")
        row = layout.row()
        row.operator("custom.resetobjtransrot")

        row = layout.row()
        row.label(text="Set Object transforms to picked Object",
                  icon='TRACKING_BACKWARDS')
        row = layout.row()
        row.prop(context.scene, "PasteDataToObject", text="From")
        row = layout.row()
        row.prop(context.scene, "CopyDataFromObject", text="To")
        row = layout.row()
        row.prop(context.scene, "locationOb_checkbox", text="Location")
        row.prop(context.scene, "rotationOb_checkbox", text="Rotation")
        row.prop(context.scene, "scaleOb_checkbox", text="Scale")
        row = layout.row()
        row.operator("custom.pasteobjtransfrompickedobject")

        row = layout.row()
        row.label(text="Delete meshes without data and others", icon='DOT')
        row = layout.row()
        row.operator("custom.deleteemptyobj")
        row = layout.row()


class Vicho_PT_vertex_color(bpy.types.Panel):
    bl_label = "Oldy Vertex Color"
    bl_idname = "VICHO_PT_vertex_color"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("vicho.vertexcolor",
                     text="Create Vertex Color", icon='COLOR')
        row = layout.row()


class Vicho_TextureDictionaryPanel(bpy.types.Panel):
    bl_label = "Texture Dictionary Tools"
    bl_idname = "VICHO_PT_texture_dictionary"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = VICHO_PT_MAIN_PANEL.bl_idname

    def draw_header(self, context):
        self.layout.label(text="", icon="TEXTURE")

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        list_col = row.column()
        scene = context.scene
        list_col.template_list("YtdList", "", scene,
                               "ytd_list", scene, "ytd_active_index")
        list_col.separator()
        row2 = list_col.row()
        row2.operator("ytd_list.add_ytd", icon='ADD', text="Create Folder from selected object(s)")
        row2.operator("ytd_list.remove_ytd", icon='REMOVE', text="Delete Folder")
        list_col.separator()
        row3 = list_col.row()
        row3.operator("ytd_list.reload_all", icon='FILE_REFRESH', text="Reload all folders in list")
        row3.operator("ytd_list.add_to_ytd", icon='IMPORT', text="Add selected object(s) to folder")
        list_col.separator()
        list_col.prop(scene, "ytd_export_path", text="Export path")
        list_col.separator()
        list_col.operator("custom.exportytdfolders",
                          text="Export YTD Folders", icon='FORCE_TEXTURE')


class F2YTD_PT_Panel_Settings(bpy.types.Panel):
    bl_label = "Folder2YTD Settings"
    bl_idname = "F2YTD_PT_Panel_Settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = Vicho_TextureDictionaryPanel.bl_idname

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
