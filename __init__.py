import bpy
import os
from mathutils import Quaternion
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from .utils.ytdHelper import *
from .utils.vichofuncs import *
import subprocess

bl_info = {
    "name": "Vicho's Misc Tools",
    "author": "Somebody",
    "version": (0, 1, 5),
    "blender": (2, 93, 0),
    "location": "View3D",
    "description": "Some tools by Vicho",
    "warning": "",
    "wiki_url": "",
    "category": "Vicho Tools",
}


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
        col = row.column(align=True)
        col.operator("ytd_list.add_ytd", icon='ADD', text="")
        col.operator("ytd_list.remove_ytd", icon='REMOVE', text="")
        list_col.separator()
        list_col.prop(scene, "ytd_export_path", text="")
        list_col.separator()
        list_col.operator("custom.exportytdfolders", text="Export YTD Folders")



class ExpSelObjsFile(bpy.types.Operator):
    bl_idname = "custom.selobjsastext"
    bl_label = "Save to file"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
        objetos = context.selected_objects
        nombres = []
        for objeto in objetos:
            nombres.append(objeto.name)
        # filter name with a dot and just get the string before the dot
        nombres = [nombre.split(".")[0] for nombre in nombres]
        nombres = list(set(nombres))
        # get user's desktop path
        desktop_path = os.path.expanduser("~/Desktop")
        # export list to file with name from scene
        with open(desktop_path + "/" + context.scene.file_name_field + ".txt", "w") as f:
            for nombre in nombres:
                f.write(nombre + "\n")

        return {'FINISHED'}


class VichoCreateVC(bpy.types.Operator):
    bl_idname = "vicho.vertexcolor"
    bl_label = "Create Vertex Color"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.geometry.color_attribute_add(
            name="colour0", domain='CORNER', data_type='BYTE_COLOR')
        return {'FINISHED'}


class ResetObjTransRot(bpy.types.Operator):
    bl_idname = "custom.resetobjtransrot"
    bl_label = "Reset object(s) transforms"

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0 and (context.scene.location_checkbox or context.scene.rotation_checkbox or context.scene.scale_checkbox)

    def execute(self, context):
        check_loc = context.scene.location_checkbox
        check_rot = context.scene.rotation_checkbox
        check_scale = context.scene.scale_checkbox

        objetos = context.selected_objects
        for objeto in objetos:
            if check_loc:
                objeto.location = (0, 0, 0)
            if check_rot:
                if objeto.rotation_mode == 'QUATERNION':
                    objeto.rotation_quaternion = (1, 0, 0, 0)
                elif objeto.rotation_mode == 'AXIS_ANGLE':
                    objeto.rotation_axis_angle = (0, 0, 0, 0)
                else:
                    objeto.rotation_euler = (0, 0, 0)

            if check_scale:
                objeto.scale = (1, 1, 1)

        return {'FINISHED'}


class ExportMLOTransFile(bpy.types.Operator):
    bl_idname = "custom.exportmlostransformstofile"
    bl_label = "Export MLO transforms to YMAP"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
        objetos = context.selected_objects

        for objeto in objetos:
            if objeto.sollum_type == 'sollumz_bound_composite' or objeto.type == 'MESH':
                export_milo_ymap_xml(
                    'Mi bro', objeto, context.scene.ymap_instance_name_field)
                self.report(
                    {'INFO'}, f"{objeto.name} location and rotation exported to file")

            else:
                self.report(
                    {'WARNING'}, f"{objeto.name} is not a Bound Composite or a Mesh")

        return {'FINISHED'}


class PasteObjectTransformFromPickedObject(bpy.types.Operator):
    bl_idname = "custom.pasteobjtransfrompickedobject"
    bl_label = "Set transforms"

    @classmethod
    def poll(cls, context):
        return context.scene.CopyDataFromObject is not None and (context.scene.locationOb_checkbox or context.scene.rotationOb_checkbox or context.scene.scaleOb_checkbox)

    def execute(self, context):
        fromobj = context.scene.CopyDataFromObject
        toobj = context.scene.PasteDataToObject

        if context.scene.locationOb_checkbox:
            toobj.location = fromobj.location
        if context.scene.rotationOb_checkbox:
            toobj.rotation_euler = fromobj.rotation_euler
        if context.scene.scaleOb_checkbox:
            toobj.scale = fromobj.scale

        return {'FINISHED'}


class DeleteEmptyObj(bpy.types.Operator):
    bl_idname = "custom.deleteemptyobj"
    bl_label = "Delete empty objects"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
        objects = context.selected_objects

        for obj in objects:
            if obj.type == 'EMPTY':
                if obj.sollum_type == 'sollumz_drawable':
                    if len(obj.children) < 1:
                        bpy.data.objects.remove(obj)
                    else:
                        for ochild in obj.children:
                            if ochild.sollum_type == 'sollumz_drawable_model':
                                drawmodelchild = ochild.children
                                if len(drawmodelchild) < 1:
                                    bpy.data.objects.remove(ochild)

                                else:

                                    for dchild in drawmodelchild:
                                        if dchild.sollum_type == 'sollumz_drawable_geometry' and dchild.type == 'MESH':
                                            if len(dchild.data.vertices) < 1:
                                                bpy.data.objects.remove(dchild)
                                                if len(ochild.children) < 1:
                                                    bpy.data.objects.remove(
                                                        ochild)

                elif obj.sollum_type == 'sollumz_bound_composite':
                    if len(obj.children) < 1:
                        bpy.data.objects.remove(obj)
                    else:
                        for ochild in obj.children:
                            if ochild.sollum_type == 'sollumz_bound_geometrybvh':
                                drawmodelchild = ochild.children
                                if len(drawmodelchild) < 1:
                                    bpy.data.objects.remove(ochild)

                                else:

                                    for dchild in drawmodelchild:
                                        if (dchild.sollum_type == 'sollumz_bound_poly_triangle' or
                                            dchild.sollum_type == 'sollumz_bound_poly_box' or
                                            dchild.sollum_type == 'sollumz_bound_poly_sphere' or
                                            dchild.sollum_type == 'sollumz_bound_poly_cylinder' or
                                                dchild.sollum_type == 'sollumz_bound_poly_capsule') and dchild.type == 'MESH':
                                            if len(dchild.data.vertices) < 1:
                                                bpy.data.objects.remove(dchild)
                                                if len(ochild.children) < 1:
                                                    bpy.data.objects.remove(
                                                        ochild)
                elif obj.sollum_type == 'sollumz_drawable_dictionary':
                    print('todo')
            else:
                continue

        return {'FINISHED'}

class YtdExportPath(bpy.types.Operator):
    bl_idname = "custom.exportytdfolders"
    bl_label = "Export YTD folders"


    @classmethod
    def poll(cls, context):
        return len(context.scene.ytd_list) > 0 and context.scene.ytd_export_path != '' and os.path.exists(context.scene.ytd_export_path)

    def execute(self, context):
        ytds = context.scene.ytd_list

        print(f'WIP {ytds}')
        ExportYTDFolders(ytds, context.scene.ytd_export_path)
        subprocess.Popen('explorer "{}"'.format(context.scene.ytd_export_path))
        return {'FINISHED'}

class MloYmapFileBrowser(bpy.types.Operator, ExportHelper):
    bl_idname = "vicho.mloyampfilebrowser"
    bl_label = "Export MLO transforms to YMAP"
    bl_action = "Export a YMAP MLO"
    bl_showtime = True

    filename_ext = '.ymap'

    filter_glob: StringProperty(
        default='*.ymap',
        options={'HIDDEN'}
    )

    def execute(self, context):
        try:
            export_milo_ymap_xml(
                self.filepath, context.active_object, context.scene.ymap_instance_name_field)
            self.report({'INFO'}, f"{self.filepath} successfully exported")
            return {'FINISHED'}

        except:
            self.report(
                {'ERROR'}, f"Error exporting {self.filepath} ")
            return {'FINISHED'}


CLASSES = [
    VICHO_PT_MAIN_PANEL,
    ExpSelObjsFile,
    ResetObjTransRot,
    ExportMLOTransFile,
    DeleteEmptyObj,
    VICHO_PT_MISC1_PANEL,
    VichoMloToolsPanel,
    VichoObjectToolsPanel,
    PasteObjectTransformFromPickedObject,
    MloYmapFileBrowser,
    Vicho_PT_vertex_color,
    VichoCreateVC,
    Vicho_TextureDictionaryPanel,
    ImageString,
    YtdList,
    YtdItem,
    YTDLIST_OT_add,
    YTDLIST_OT_remove,
    YtdExportPath
]


def register():
    for klass in CLASSES:
        bpy.utils.register_class(klass)

    bpy.types.Scene.ytd_list = bpy.props.CollectionProperty(type=YtdItem)
    bpy.types.Scene.ytd_active_index = bpy.props.IntProperty()

def unregister():
    for klass in CLASSES:
        bpy.utils.unregister_class(klass)
    
    del bpy.types.Scene.ytd_list
    del bpy.types.Scene.ytd_active_index


if __name__ == '__main__':
    register()
