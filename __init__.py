from ast import Try
import bpy
import os
import xml.dom.minidom as md
from mathutils import Quaternion
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator

bl_info = {
    "name": "Vicho's Misc Tools",
    "author": "Somebody",
    "version": (0, 1, 3),
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
        return context.scene.CopyDataFromObject is not None and (context.scene.PasteDataToObject or context.scene.locationOb_checkbox or context.scene.rotationOb_checkbox or context.scene.scaleOb_checkbox)

    def execute(self, context):
        fromobj = context.scene.CopyDataFromObject
        toobj = context.scene.PasteDataToObject

        toobj.location = fromobj.location
        toobj.rotation_euler = fromobj.rotation_euler
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
            



def export_milo_ymap_xml(ymapname, object, instance_name):

    root = md.Document()

    xml = root.createElement('CMapData')
    root.appendChild(xml)

    ymapName = root.createElement('name')
    ymapName.appendChild(root.createTextNode(
        os.path.basename(ymapname.split('.')[0])))
    xml.appendChild(ymapName)

    parent = root.createElement('parent')
    xml.appendChild(parent)

    flags = root.createElement('flags')
    flags.setAttribute('value', '0')
    xml.appendChild(flags)

    contentFlags = root.createElement('contentFlags')
    contentFlags.setAttribute('value', '9')
    xml.appendChild(contentFlags)

    streamingExtentsMin = root.createElement('streamingExtentsMin')
    streamingExtentsMin.setAttribute('x', '0')
    streamingExtentsMin.setAttribute('y', '0')
    streamingExtentsMin.setAttribute('z', '0')
    xml.appendChild(streamingExtentsMin)

    streamingExtentsMax = root.createElement('streamingExtentsMax')
    streamingExtentsMax.setAttribute('x', '0')
    streamingExtentsMax.setAttribute('y', '0')
    streamingExtentsMax.setAttribute('z', '0')
    xml.appendChild(streamingExtentsMax)

    entitiesExtentsMin = root.createElement('entitiesExtentsMin')
    entitiesExtentsMin.setAttribute('x', '0')
    entitiesExtentsMin.setAttribute('y', '0')
    entitiesExtentsMin.setAttribute('z', '0')
    xml.appendChild(entitiesExtentsMin)

    entitiesExtentsMax = root.createElement('entitiesExtentsMax')
    entitiesExtentsMax.setAttribute('x', '0')
    entitiesExtentsMax.setAttribute('y', '0')
    entitiesExtentsMax.setAttribute('z', '0')
    xml.appendChild(entitiesExtentsMax)

    entities = root.createElement('entities')

    Item = root.createElement('Item')
    Item.setAttribute('type', 'CMloInstanceDef')
    entities.appendChild(Item)

    archetypeName = root.createElement('archetypeName')
    archetypeName.appendChild(root.createTextNode(instance_name))
    Item.appendChild(archetypeName)

    itemFlags = root.createElement('flags')
    itemFlags.setAttribute('value', '1572865')
    Item.appendChild(itemFlags)

    itemGuid = root.createElement('guid')
    itemGuid.setAttribute('value', '0')
    Item.appendChild(itemGuid)

    itemPosition = root.createElement('position')
    itemPosition.setAttribute('x', str(object.location[0]))
    itemPosition.setAttribute('y', str(object.location[1]))
    itemPosition.setAttribute('z', str(object.location[2]))
    Item.appendChild(itemPosition)

    itemRotation = root.createElement('rotation')
    itemRotation.setAttribute(
        'x', str(object.rotation_euler.to_quaternion().x))
    itemRotation.setAttribute(
        'y', str(object.rotation_euler.to_quaternion().y))
    itemRotation.setAttribute(
        'z', str(object.rotation_euler.to_quaternion().z))
    itemRotation.setAttribute(
        'w', str(object.rotation_euler.to_quaternion().w))

    Item.appendChild(itemRotation)

    itemScaleXY = root.createElement('scaleXY')
    itemScaleXY.setAttribute('value', '1')
    Item.appendChild(itemScaleXY)

    itemScaleZ = root.createElement('scaleZ')
    itemScaleZ.setAttribute('value', '1')
    Item.appendChild(itemScaleZ)

    itemParentIndex = root.createElement('parentIndex')
    itemParentIndex.setAttribute('value', '-1')
    Item.appendChild(itemParentIndex)

    itemLodDist = root.createElement('lodDist')
    itemLodDist.setAttribute('value', '700')
    Item.appendChild(itemLodDist)

    itemchildLodDist = root.createElement('childLodDist')
    itemchildLodDist.setAttribute('value', '0')
    Item.appendChild(itemchildLodDist)

    itemlodLevel = root.createElement('lodLevel')
    itemlodLevel.appendChild(root.createTextNode('LODTYPES_DEPTH_ORPHANHD'))
    Item.appendChild(itemlodLevel)

    itennumChildren = root.createElement('numChildren')
    itennumChildren.setAttribute('value', '0')
    Item.appendChild(itennumChildren)

    itempriorityLevel = root.createElement('priorityLevel')
    itempriorityLevel.appendChild(root.createTextNode('PRI_REQUIRED'))
    Item.appendChild(itempriorityLevel)

    itemextensions = root.createElement('extensions')
    Item.appendChild(itemextensions)

    itemambientOcclusionMultiplier = root.createElement(
        'ambientOcclusionMultiplier')
    itemambientOcclusionMultiplier.setAttribute('value', '255')
    Item.appendChild(itemambientOcclusionMultiplier)

    itemartificialAmbientOcclusion = root.createElement(
        'artificialAmbientOcclusion')
    itemartificialAmbientOcclusion.setAttribute('value', '255')
    Item.appendChild(itemartificialAmbientOcclusion)

    itemtintValue = root.createElement('tintValue')
    itemtintValue.setAttribute('value', '0')
    Item.appendChild(itemtintValue)

    itemgroupId = root.createElement('groupId')
    itemgroupId.setAttribute('value', '0')
    Item.appendChild(itemgroupId)

    itemfloorId = root.createElement('floorId')
    itemfloorId.setAttribute('value', '0')
    Item.appendChild(itemfloorId)

    itemdefaultEntitySets = root.createElement('defaultEntitySets')
    Item.appendChild(itemdefaultEntitySets)

    itemnumExitPortals = root.createElement('numExitPortals')
    itemnumExitPortals.setAttribute('value', '0')
    Item.appendChild(itemnumExitPortals)

    itemMLOInstflags = root.createElement('MLOInstflags')
    itemMLOInstflags.setAttribute('value', '0')
    Item.appendChild(itemMLOInstflags)
    xml.appendChild(entities)

    xml_str = xml.toprettyxml(indent='\t')
    save_path = ymapname + '.xml'

    with open(save_path, 'w') as f:
        f.write(xml_str)
        f.close()


def get_textures_from_the_material(blender_material):
    textures = []
    if blender_material:
        if blender_material.node_tree:
            for tn in blender_material.node_tree.nodes:
                if tn.type == 'TEX_IMAGE':
                    textures.append(tn)
    return textures


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
    MloYmapFileBrowser

]


def register():
    for klass in CLASSES:
        bpy.utils.register_class(klass)
    bpy.types.Scene.file_name_field = bpy.props.StringProperty(
        name="File Name",
        default="",
        description="File name for the text file",
        maxlen=50)

    bpy.types.Scene.ymap_instance_name_field = bpy.props.StringProperty(
        name="Instance Name",
        default="",
        description="instance name for the MLO Instance",
        maxlen=50)
    bpy.types.Scene.location_checkbox = bpy.props.BoolProperty(
        name="Reset Location",
        description="Reset location")
    bpy.types.Scene.rotation_checkbox = bpy.props.BoolProperty(
        name="Reset Rotation",
        description="Reset rotation")
    bpy.types.Scene.scale_checkbox = bpy.props.BoolProperty(
        name="Reset Scale",
        description="Reset scale")
    bpy.types.Scene.CopyDataFromObject = bpy.props.PointerProperty(
        name="Copy Data From Object",
        type=bpy.types.Object)
    bpy.types.Scene.PasteDataToObject = bpy.props.PointerProperty(
        name="Paste Data To Object",
        type=bpy.types.Object)

    bpy.types.Scene.locationOb_checkbox = bpy.props.BoolProperty(
        name="Location",
        description="Location")
    bpy.types.Scene.rotationOb_checkbox = bpy.props.BoolProperty(
        name="Rotation",
        description="Rotation")
    bpy.types.Scene.scaleOb_checkbox = bpy.props.BoolProperty(
        name="Scale",
        description="Scale")


def unregister():
    for klass in CLASSES:
        bpy.utils.unregister_class(klass)
    del bpy.types.Scene.file_name_field
    del bpy.types.Scene.ymap_instance_name_field
    del bpy.types.Scene.location_checkbox
    del bpy.types.Scene.rotation_checkbox
    del bpy.types.Scene.scale_checkbox
    del bpy.types.Scene.CopyDataFromObject
    del bpy.types.Scene.PasteDataToObject
    del bpy.types.Scene.locationOb_checkbox
    del bpy.types.Scene.rotationOb_checkbox
    del bpy.types.Scene.scaleOb_checkbox


if __name__ == '__main__':
    register()
