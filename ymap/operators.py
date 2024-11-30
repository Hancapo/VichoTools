import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty
from .funcs import add_ymap_to_scene, remove_ymap_from_scene
import os

class VICHO_OT_import_ymap(bpy.types.Operator, ImportHelper):
    """Import YMAP file(s)"""
    bl_idname = "ymap.import_ymap"
    bl_label = "Import YMAP file(s)"

    filename_ext = ".ymap"
    
    filter_glob: StringProperty(
        default="*.ymap",
        options={"HIDDEN"}
    )
    files: bpy.props.CollectionProperty(type=bpy.types.OperatorFileListElement)
    
    directory: StringProperty(maxlen=1024, default="", subtype='DIR_PATH')
    
    show_import: BoolProperty(name="Show Include", default=True)
    
    import_entities: BoolProperty(name="Entities", default=True, description="Import entities from the YMAP file(s)")
    import_occluders: BoolProperty(name="Occluders", default=True, description="Import occluders including box and model occluders from the YMAP file(s)")
    import_extensions: BoolProperty(name="Entity Extensions", default=True, description="Import entity extensions from the YMAP file(s)")
    import_timecycle_mods: BoolProperty(name="Timecycle Modifiers", default=True, description="Import timecycle modifiers from the YMAP file(s)")
    import_car_generators: BoolProperty(name="Car Generators", default=True, description="Import car generators from the YMAP file(s)")

    def execute(self, context):
        scene = context.scene
        for file in self.files:
            filepath: str = os.path.join(self.directory, file.name)
            add_ymap_to_scene(scene, filepath, self)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        row = box.row()
        row.prop(self, "show_import", text="Include", icon='TRIA_DOWN' if self.show_import else 'TRIA_RIGHT', emboss=False)
        
        if self.show_import:
            col = box.column(align=True)
            col.prop(self, "import_entities", icon="OUTLINER_OB_GROUP_INSTANCE")
            col.prop(self, "import_occluders", icon="GP_CAPS_ROUND")
            col.prop(self, "import_extensions", icon="MODIFIER")
            col.prop(self, "import_timecycle_mods", icon="TIME")
            col.prop(self, "import_car_generators", icon="AUTO")

class VICHO_OT_remove_ymap(bpy.types.Operator):
    """Remove YMAP file(s)"""
    bl_idname = "ymap.remove_ymap"
    bl_label = "Remove YMAP file(s)"
    
    @classmethod
    def poll(cls, context):
        return context.scene.ymap_list_index >= 0
    
    def execute(self, context):
        scene = context.scene
        selected_ymap_index = scene.ymap_list_index
        if remove_ymap_from_scene(scene, selected_ymap_index):
            self.report({'INFO'}, f"YMAP removed from scene")
        else:
            self.report({'ERROR'}, f"Error removing YMAP from scene")
        return {'FINISHED'}