import subprocess
import bpy
import os

from .tools.vicho_funcs import export_milo_ymap_xml
from .ytd.ytd_helper import ExportYTD_Folders, ExportYTD_Files
from bpy.props import StringProperty
from bpy_extras.io_utils import ExportHelper


class ExpSelObjsFile(bpy.types.Operator):
    bl_idname = "vicho.selobjsastext"
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
    bl_idname = "vicho.resetobjtransrot"
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
    bl_idname = "vicho.exportmlostransformstofile"
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
    bl_idname = "vicho.pasteobjtransfrompickedobject"
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
    bl_idname = "vicho.deleteemptyobj"
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
