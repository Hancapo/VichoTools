import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty
from .funcs import add_ymap_to_list

class VICHO_OT_import_ymap(bpy.types.Operator, ImportHelper):
    """Import a YMAP file"""
    bl_idname = "ymap.import_ymap"
    bl_label = "Import a YMAP file"

    filename_ext = ".ymap"
    
    filter_glob: StringProperty(
        default="*.ymap",
        options={"HIDDEN"}
    )
    files: bpy.props.CollectionProperty(type=bpy.types.OperatorFileListElement)
    
    show_import: BoolProperty(name="Show Include", default=True)
    
    import_entities: BoolProperty(name="Entities", default=True, description="Import entities from the YMAP file(s)")
    import_occluders: BoolProperty(name="Occluders", default=True, description="Import occluders including box and model occluders from the YMAP file(s)")
    import_extensions: BoolProperty(name="Entity Extensions", default=True, description="Import entity extensions from the YMAP file(s)")
    import_timecycle_mods: BoolProperty(name="Timecycle Modifiers", default=True, description="Import timecycle modifiers from the YMAP file(s)")
    import_car_generators: BoolProperty(name="Car Generators", default=True, description="Import car generators from the YMAP file(s)")

    def execute(self, context):
        for file in self.files:
            add_ymap_to_list(context.scene, file, self)
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
            col.prop(self, "import_entities")
            col.prop(self, "import_occluders")
            col.prop(self, "import_entity_extensions")
            col.prop(self, "import_timecycle_modifiers")
            col.prop(self, "import_car_generators")
