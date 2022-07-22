import bpy
import os

bl_info = {
    "name": "Vicho's Misc Tools",
    "author": "Somebody",
    "version": (0, 0, 5),
    "blender": (2, 93, 0),
    "location": "View3D",
    "description": "Some tools for Vicho",
    "warning": "",
    "wiki_url": "",
    "category": "Misc Tools",
}

class VichoToolsPanel(bpy.types.Panel):
    bl_label = "Misc Tools 1" 
    bl_idname = "MAINMISCTOOLS_PT_"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Misc Tools"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Save selected object(s) as unique list to file:", icon='ALIGN_RIGHT')
        row = layout.row()
        row.prop(context.scene, "file_name_field", text="File name")
        row = layout.row()
        row.operator("custom.selobjsastext")
        row = layout.row()
        row.label(text="Export selected object(s) as IPL file:", icon='FILE_NEW')
        row = layout.row()
        row.prop(context.scene, "ipl_name_field", text="IPL Name")
        row = layout.row()
        row.operator("custom.exportallobjstoipl")
        row = layout.row()
        row.label(text="Reset Object(s) transform:", icon='PLAY_REVERSE')
        row = layout.row()
        row.prop(context.scene, "location_checkbox", text="Reset Location")
        row.prop(context.scene, "rotation_checkbox", text="Reset Rotation")
        row.prop(context.scene, "scale_checkbox", text="Reset Scale")
        row = layout.row()
        row.operator("custom.resetobjtransrot")
        row = layout.row()
        row.label(text="MLO Misc tools:", icon="MOD_DECIM")
        row = layout.row()
        row.operator("custom.exportmlostransformstofile")
        row = layout.row()
        #create centered label
        row.label(text="Object misc tools:", icon='OBJECT_DATAMODE')
        row = layout.row()
        row.label(text="Set Object transforms to picked Object", icon='TRACKING_BACKWARDS')
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
    bl_label = "Export all objects to IPL"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None

    def execute(self, context):
        objetos = context.selected_objects
        #get quaternion from object
        desktop_path = os.path.expanduser("~/Desktop")


        with open(desktop_path + "/" + context.scene.ipl_name_field + ".ipl", "w") as f:
            f.write("inst")
            f.write("\n")
            for objeto in objetos:
                quaternion_objeto = objeto.rotation_quaternion
                nombre_objeto = objeto.name
                #if object name contains a dot get the string before the dot
                if "." in nombre_objeto:
                    nombre_objeto = objeto.name.split(".")[0]
                f.write(f"9999, {nombre_objeto}, 1, {objeto.location[0]}, {objeto.location[1]}, {objeto.location[2]}, {quaternion_objeto[1]}, {quaternion_objeto[2]}, {quaternion_objeto[3]}, {quaternion_objeto[0]}, 0\n")
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
                objeto.rotation_euler = (0, 0, 0)
            if check_scale == True:
                objeto.scale = (1, 1, 1)
            
        return {'FINISHED'}

class ExportMLOTransFile(bpy.types.Operator):
    bl_idname = "custom.exportmlostransformstofile"
    bl_label = "Export MLO(s) transforms to file"
    
    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None
    
    def execute(self, context):
        objetos = context.selected_objects

        for objeto in objetos:
            if objeto.sollum_type == 'sollumz_bound_composite' or objeto.type == 'MESH':
                #export object location and rotation (in quaternion) to file in selected folder
                desktop_path = os.path.expanduser("~/Desktop")
                with open(desktop_path + "/" + "MloData.txt", "w") as f:
                    f.write(f"{objeto.name}")
                    f.write("\n")
                    f.write(f"{objeto.location[0]}, {objeto.location[1]}, {objeto.location[2]}")
                    f.write("\n")
                    f.write(f"{objeto.rotation_quaternion[1]}, {objeto.rotation_quaternion[2]}, {objeto.rotation_quaternion[3] * -1}, {objeto.rotation_quaternion[0]}")
                    f.write("\n")
                f.close()
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

CLASSES = [
    ExpSelObjsFile,
    IplExportOperator,
    ResetObjTransRot,
    ExportMLOTransFile,
    VichoToolsPanel,
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