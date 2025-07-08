import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty
from .funcs import import_ymap_to_scene, remove_ymap_from_scene, create_ymap_empty
import os
import time
from .helper import str_loaded_count
from bpy.types import Object
from .constants import COMPAT_SOLL_TYPES

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
    import_props: BoolProperty(name="Import Props", default=True, description="Whether or not to import props from the YMAP file(s)")
    
    @classmethod
    def poll(cls, context):
        return str_loaded_count() > 0

    def execute(self, context):
        scene = context.scene
        start_time = time.time()
        for file in self.files:
            filepath: str = os.path.join(self.directory, file.name)
            import_ymap_to_scene(scene, filepath, self.import_entities, self.import_occluders, self.import_timecycle_mods, self.import_car_generators, self.import_props, self, self.asset_path)
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
                col.prop(self, "asset_path", icon="FILE_FOLDER")
                col.separator()
                col.prop(self, "import_props")

class VICHO_OT_remove_ymap(bpy.types.Operator):
    """Remove YMAP item from the scene"""
    bl_idname = "ymap.remove_ymap"
    bl_label = "Remove YMAP item from the scene"
    
    @classmethod
    def poll(cls, context):
        return len(context.scene.ymap_list) > 0
    
    def execute(self, context):
        scene = context.scene
        selected_ymap_index = scene.ymap_list_index 
        if remove_ymap_from_scene(scene, selected_ymap_index):
            self.report({'INFO'}, f"YMAP removed from scene")
        else:
            self.report({'ERROR'}, f"Error removing YMAP from scene")
        return {'FINISHED'}
    
    # Confirmation dialog
    def invoke(self, context, event):
        scene = context.scene
        selected_ymap_index = scene.ymap_list_index
        ymap_name = scene.ymap_list[selected_ymap_index].ymap_object.name if selected_ymap_index >= 0 else "YMAP"
        message = f"Are you sure you want to remove the YMAP '{ymap_name}' from the scene?"
        return context.window_manager.invoke_confirm(self, event, message=message)
    
    
class VICHO_OT_add_ymap(bpy.types.Operator):
    """Add YMAP item to the scene"""
    bl_idname = "ymap.add_ymap"
    bl_label = "Add YMAP item to the scene"
    
    def execute(self, context):
        scene = context.scene
        new_ymap = scene.ymap_list.add()
        new_ymap.ymap_object = create_ymap_empty("New YMAP")
        scene.ymap_list_index = len(scene.ymap_list) - 1
        bpy.ops.ymap.map_data_menu(operator_id="ymap.map_data_menu")
        self.report({'INFO'}, f"YMAP added to scene")
        

class VICHO_OT_add_entity(bpy.types.Operator):
    """Add entity to the YMAP"""
    bl_idname = "ymap.add_entity"
    bl_label = "Add entity to YMAP"
    
    def execute(self, context):
        scene = context.scene
        selected_objs: list[Object] = [obj for obj in bpy.context.selected_objects if obj.type == 'EMPTY' and obj.sollum_type in COMPAT_SOLL_TYPES]
        added_entities: str = ""
        for obj in selected_objs:
            new_entity = scene.ymap_list[scene.ymap_list_index].entities.add()
            new_entity.linked_object = obj
            scene.entity_list_index = len(scene.ymap_list[scene.ymap_list_index].entities) - 1
            added_entities += f"{obj.name}, "
        self.report({'INFO'}, f"Entities added to YMAP: {added_entities}")
        return {'FINISHED'}    
            
    
class VICHO_OT_go_to_entity(bpy.types.Operator):
    """Go to entity"""
    bl_idname = "ymap.go_to_entity"
    bl_label = "Go to entity"
    
    def execute(self, context):
        scene = context.scene
        selected_ymap_index = scene.ymap_list_index
        ymap = scene.ymap_list[selected_ymap_index]
        entity = ymap.entities[scene.entity_list_index]
        
        if entity.linked_object:
            bpy.context.view_layer.objects.active = entity.linked_object
            bpy.ops.object.select_all(action='DESELECT')
            entity.linked_object.select_set(True)
            bpy.ops.view3d.view_selected()
        
        return {'FINISHED'}