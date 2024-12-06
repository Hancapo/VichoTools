import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty
from .funcs import add_ymap_to_scene, remove_ymap_from_scene
import os
import time

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
    show_assets: BoolProperty(name="Show Assets", default=True)
    
    import_entities: BoolProperty(name="Entities", default=True, description="Import entities from the YMAP file(s)")
    import_occluders: BoolProperty(name="Occluders", default=True, description="Import occluders including box and model occluders from the YMAP file(s)")
    import_extensions: BoolProperty(name="Entity Extensions", default=True, description="Import entity extensions from the YMAP file(s)")
    import_timecycle_mods: BoolProperty(name="Timecycle Modifiers", default=True, description="Import timecycle modifiers from the YMAP file(s)")
    import_car_generators: BoolProperty(name="Car Generators", default=True, description="Import car generators from the YMAP file(s)")
    
    asset_path: StringProperty(name="Asset Path", default="")
    import_assets: BoolProperty(name="Import Assets", default=True, description="Import assets from the YMAP file(s)")

    def execute(self, context):
        scene = context.scene
        start_time = time.time()
        for file in self.files:
            filepath: str = os.path.join(self.directory, file.name)
            add_ymap_to_scene(scene, filepath, self.import_entities, self.import_occluders, self.import_timecycle_mods, self.import_car_generators, self, self.asset_path)
        self.report({'INFO'}, f"YMAP file(s) imported in {time.time() - start_time:.2f} seconds")
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
            
        
        
        if self.import_entities:
            box = layout.box()
            row = box.row()
            row.prop(self, "show_assets", text="Assets", icon='TRIA_DOWN' if self.show_assets else 'TRIA_RIGHT', emboss=False)
            if self.show_assets:
                col = box.column(align=True)
                col.prop(self, "import_assets")
                col.separator()
                col.prop(self, "asset_path", icon="FILE_FOLDER")

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
    
class VICHO_OT_go_to_entity(bpy.types.Operator):
    """Go to entity"""
    bl_idname = "ymap.go_to_entity"
    bl_label = "Go to entity"
    
    def execute(self, context):
        scene = context.scene
        selected_ymap_index = scene.ymap_list_index
        ymap = scene.fake_ymap_list[selected_ymap_index]
        entity = ymap.entities[scene.entity_list_index]
        
        if entity.linked_object:
            bpy.context.view_layer.objects.active = entity.linked_object
            bpy.ops.object.select_all(action='DESELECT')
            entity.linked_object.select_set(True)
            bpy.ops.view3d.view_selected()
        
        return {'FINISHED'}