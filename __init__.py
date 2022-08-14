import bpy
import os
import xml.dom.minidom as md
from mathutils import Quaternion

bl_info = {
    "name": "Vicho's Misc Tools",
    "author": "Somebody",
    "version": (0, 0, 9),
    "blender": (2, 93, 0),
    "location": "View3D",
    "description": "Some tools by Vicho",
    "warning": "",
    "wiki_url": "",
    "category": "Vicho Tools",
}

class VichoMisc1ToolsPanel(bpy.types.Panel):
    bl_label = "Misc Tools 1" 
    bl_idname = "MAINMISCTOOLS_PT_"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Misc Tools"

    def draw(self, context):
        layout = self.layout
        #Create category
        box = layout.box()
        row = box.row()
        row.label(text="Save selected object(s) as unique list to file:", icon='ALIGN_RIGHT')
        row = box.row()
        row.prop(context.scene, "file_name_field", text="File name")
        row = box.row()
        row.operator("custom.selobjsastext")
        row = box.row()

class VichoMloToolsPanel(bpy.types.Panel):
    bl_label = "MLO Tools" 
    bl_idname = "VICMLOTOOLS_PT_"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Misc Tools"

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.prop(context.scene, "ymap_mlo_name_field", text="YMAP name")
        row = box.row()
        row.prop(context.scene, "ymap_instance_name_field", text="Instance name")
        row = box.row()
        row.operator("custom.exportmlostransformstofile")

class VichoObjectToolsPanel(bpy.types.Panel):
    bl_label = "Object Tools" 
    bl_idname = "VICHOBJECTTOOLS_PT_"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Misc Tools"

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.label(text="Reset Object(s) transform:", icon='PLAY_REVERSE')
        row = box.row()
        row.prop(context.scene, "location_checkbox", text="Reset Location")
        row.prop(context.scene, "rotation_checkbox", text="Reset Rotation")
        row.prop(context.scene, "scale_checkbox", text="Reset Scale")
        row = box.row()
        row.operator("custom.resetobjtransrot")
        row = box.row()

        box = layout.box()
        row = box.row()
        row.label(text="Set Object transforms to picked Object", icon='TRACKING_BACKWARDS')
        row = box.row()
        row.prop(context.scene, "PasteDataToObject", text="From")
        row = box.row()
        row.prop(context.scene, "CopyDataFromObject", text="To")
        row = box.row()
        row.prop(context.scene, "locationOb_checkbox", text="Location")
        row.prop(context.scene, "rotationOb_checkbox", text="Rotation")
        row.prop(context.scene, "scaleOb_checkbox", text="Scale")
        row = box.row()
        row.operator("custom.pasteobjtransfrompickedobject")

        box = layout.box()
        row = box.row()
        row.label(text="Delete meshes without data and others", icon='DOT')
        row = box.row()
        row.operator("custom.deleteemptyobj")
        row = box.row()



class VichoPlacementToolsPanel(bpy.types.Panel):
    bl_label = "Placement Tools" 
    bl_idname = "VICHOPLACEMENTTOOLS_PT_"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Misc Tools"

    def draw(self, context):
        layout = self.layout
        box = layout.box()

        
        row = box.row()
        row.label(text="Export selected object(s) as IPL file:", icon='FILE_NEW')
        row = box.row()
        row.prop(context.scene, "ipl_name_field", text="IPL Name")
        row = box.row()
        row.operator("custom.exportallobjstoipl")
        row = box.row()

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
        #filter name with a dot and just get the string before the dot
        nombres = [nombre.split(".")[0] for nombre in nombres]
        nombres = list(set(nombres))
        #get user's desktop path
        desktop_path = os.path.expanduser("~/Desktop")
        #export list to file with name from scene
        with open(desktop_path + "/" + context.scene.file_name_field + ".txt", "w") as f:
            for nombre in nombres:
                f.write(nombre + "\n")
        

        return {'FINISHED'}

class IplExportOperator(bpy.types.Operator):
    bl_idname = "custom.exportallobjstoipl"
    bl_label = "Export selected objects to IPL"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
        objetos = context.selected_objects
        desktop_path = os.path.expanduser("~/Desktop")


        with open(desktop_path + "/" + context.scene.ipl_name_field + ".ipl", "w") as f:
            f.write("inst")
            f.write("\n")
            for objeto in objetos:
                quaternion_objeto = objeto.rotation_euler.to_quaternion()
                nombre_objeto = objeto.name
                #if object name contains a dot get the string before the dot
                if "." in nombre_objeto:
                    nombre_objeto = objeto.name.split(".")[0]
                f.write(f"9999, {nombre_objeto}, 1, {objeto.location[0]}, {objeto.location[1]}, {objeto.location[2]}, {quaternion_objeto[1]}, {quaternion_objeto[2]}, {quaternion_objeto[3] * -1}, {quaternion_objeto[0]}, 0\n")
            f.write("end")
        #close file
        f.close()
        return {'FINISHED'}

class ResetObjTransRot(bpy.types.Operator):
    bl_idname = "custom.resetobjtransrot"
    bl_label = "Reset object(s) transforms"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None and (context.scene.location_checkbox or context.scene.rotation_checkbox or context.scene.scale_checkbox)

    def execute(self, context):
        check_loc = context.scene.location_checkbox
        check_rot = context.scene.rotation_checkbox
        check_scale = context.scene.scale_checkbox

        objetos = context.selected_objects
        for objeto in objetos:
            if check_loc == True:
                objeto.location = (0, 0, 0)
            if check_rot == True:
                if objeto.rotation_mode == 'QUATERNION':
                    objeto.rotation_quaternion = (1, 0, 0, 0)
                elif objeto.rotation_mode == 'AXIS_ANGLE':
                    objeto.rotation_axis_angle = (0, 0, 0, 0)
                else:
                    objeto.rotation_euler = (0, 0, 0)
                    
            if check_scale == True:
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
                export_milo_ymap_xml(context.scene.ymap_mlo_name_field, objeto, context.scene.ymap_instance_name_field)
                self.report({'INFO'}, f"{objeto.name} location and rotation exported to file")
            
            else:
                self.report({'WARNING'}, f"{objeto.name} is not a Bound Composite or a Mesh")
                
                
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
        return context.scene.objects is not None

    def execute(self, context):
        objects = context.scene.objects
        for obj in objects:
            if obj.type == 'MESH' and obj.sollum_type == 'sollumz_drawable_geometry':
                if len(obj.data.vertices) == 0:
                    bpy.data.objects.remove(obj)
        #Count verts from children inside the parent with sollum_type = 'sollumz_drawable_model'
        for obj in objects:

            if obj.sollum_type == 'sollumz_drawable_model':
                obj_total_verts = 0
                for child in obj.children:
                    if child.type == 'MESH' and child.sollum_type == 'sollumz_drawable_geometry':
                        obj_total_verts += len(child.data.vertices)
                    
                if obj_total_verts == 0:
                    bpy.data.objects.remove(obj)
        return {'FINISHED'}

def export_milo_ymap_xml(ymapname, object, instance_name):

    root = md.Document()

    xml = root.createElement('CMapData')
    root.appendChild(xml)

    ymapName = root.createElement('name')
    ymapName.appendChild(root.createTextNode(os.path.basename(ymapname)))
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
    itemRotation.setAttribute('x', str(object.rotation_euler.to_quaternion().x))
    itemRotation.setAttribute('y', str(object.rotation_euler.to_quaternion().y))
    itemRotation.setAttribute('z', str(object.rotation_euler.to_quaternion().z))
    itemRotation.setAttribute('w', str(object.rotation_euler.to_quaternion().w))

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


    itemambientOcclusionMultiplier = root.createElement('ambientOcclusionMultiplier')
    itemambientOcclusionMultiplier.setAttribute('value', '255')
    Item.appendChild(itemambientOcclusionMultiplier)

    itemartificialAmbientOcclusion = root.createElement('artificialAmbientOcclusion')
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
    

    desktop_path = os.path.expanduser("~/Desktop")

    save_path = desktop_path + "/" + ymapname + '.ymap.xml'


    with open(save_path, 'w') as f:
        f.write(xml_str)
        f.close()

CLASSES = [
    ExpSelObjsFile,
    IplExportOperator,
    ResetObjTransRot,
    ExportMLOTransFile,
    DeleteEmptyObj,
    VichoMisc1ToolsPanel,
    VichoMloToolsPanel,
    VichoPlacementToolsPanel,
    VichoObjectToolsPanel,
    PasteObjectTransformFromPickedObject

]

def register():
    for klass in CLASSES:
        bpy.utils.register_class(klass)
    bpy.types.Scene.file_name_field = bpy.props.StringProperty(
        name="File Name", 
        default="",
        description="File name for the text file",
        maxlen=50)

    bpy.types.Scene.ymap_mlo_name_field = bpy.props.StringProperty(
        name="YMAP Name",
        default="",
        description="YMAP name for the MLO Instance",
        maxlen=50)

    bpy.types.Scene.ymap_instance_name_field = bpy.props.StringProperty(
        name="Instance Name",
        default="",
        description="instance name for the MLO Instance",
        maxlen=50)
    bpy.types.Scene.ipl_name_field = bpy.props.StringProperty(
        name="IPL Name",
        default="",
        description="IPL name for the IPL file",
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
    del bpy.types.Scene.ymap_mlo_name_field
    del bpy.types.Scene.ymap_instance_name_field
    del bpy.types.Scene.ipl_name_field
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