from bpy.types import Object
from bpy.props import BoolProperty
import bpy
from ..helper import YmapData, get_entity_sets_from_entity
from ..constants import COMPAT_SOLL_TYPES
from ...misc.funcs import delete_hierarchy
from ..funcs import get_soll_parent

class VICHO_OT_add_entity(bpy.types.Operator, YmapData):
    """Adds a new entity to the YMAP"""
    bl_idname = "ymap.add_entity"
    bl_label = "Creates a new entity"
    
    @classmethod
    def poll(cls, context):
        scene = context.scene
        return len(scene.ymap_list) > 0 and scene.ymap_list[scene.ymap_list_index].ymap_object

    def execute(self, context):
        scene = context.scene
        ymap, ymap_obj, ymap_eg = self.get_ymap(context), self.get_ymap_obj(context), self.get_ymap_ent_group_obj(context)
        ymap.ymap_entity_group_object = ymap_eg
        if ymap_obj:
            new_entity = ymap.entities.add()
            new_entity.name = "New Entity"
            new_entity.flags.total_flags = 1572864
            scene.entity_list_index = len(ymap.entities) - 1
            self.report({'INFO'}, f"Added new entity to {ymap_obj.name} YMAP")
            return {'FINISHED'}

class VICHO_OT_add_entity_from_selection(bpy.types.Operator, YmapData):
    """Add(s) selected objects as entities to the YMAP"""
    bl_idname = "ymap.add_sel_objs_as_entity"
    bl_label = "Add entities from selection"
    
    @classmethod
    def poll(cls, context):
        scene = context.scene
        return cls.ymap_count(None, context) > 0 and scene.ymap_list[scene.ymap_list_index].ymap_object

    def execute(self, context):
        scene = context.scene
        selected_objs: list[Object] = [obj for obj in bpy.context.selected_objects if obj.type == 'EMPTY' and obj.sollum_type in COMPAT_SOLL_TYPES]
        ymap, ymap_obj, ymap_eg = self.get_ymap(context), self.get_ymap_obj(context), self.get_ymap_ent_group_obj(context)
        if ymap_obj:
            added_entities: str = ""
            self.get_ymap(context).ymap_entity_group_object = ymap_eg
            for obj in selected_objs:
                obj.parent = ymap_eg
                new_entity = scene.ymap_list[scene.ymap_list_index].entities.add()
                new_entity.linked_object = obj
                new_entity.linked_object.vicho_ymap_parent = ymap_obj
                new_entity.flags.total_flags = 1572864  # Default flags
                new_entity.is_mlo_instance = True if obj.sollum_type == 'sollumz_bound_composite' else False
                scene.entity_list_index = len(ymap.entities) - 1
                added_entities += f"{obj.name}, "
            self.report({'INFO'}, f"Entities added to {ymap_obj.name} YMAP: {added_entities}")
            return {'FINISHED'}

class VICHO_OT_remove_entity(bpy.types.Operator, YmapData):
    """Removes the selected entity from the entity list"""
    bl_idname = "ymap.remove_entity"
    bl_label = "Removes an entity"
    
    delete_obj_from_scene: BoolProperty(
        name="Delete Object",
        default=False,
        description="Whether to delete the linked object from the scene when removing the entity",
    ) # type: ignore
    
    can_delete: BoolProperty(
        name="Can Delete",
        default=True,
        description="Whether the entity can be deleted",
    )
    
    @classmethod
    def poll(cls, context):
        return len(context.scene.ymap_list[context.scene.ymap_list_index].entities) > 0
    
    def execute(self, context):
        if self.can_delete:
            scene = context.scene
            selected_entity_index = scene.entity_list_index
            ymap, entity = self.get_ymap(context), self.get_ent(context)
            if entity.linked_object:
                saved_name: str = entity.linked_object.name
                if self.delete_obj_from_scene:
                    delete_hierarchy(entity.linked_object)
                else:
                    entity.linked_object.parent = None
                    entity.linked_object.vicho_ymap_parent = None
                self.report({'INFO'}, f"Entity {saved_name} removed from YMAP")
            else:
                self.report({'INFO'}, "Entity removed from YMAP")
            ymap.entities.remove(selected_entity_index)
            scene.entity_list_index = max(0, selected_entity_index - 1)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

    def invoke(self, context, event):
        entity = self.get_ent(context)
        if entity.linked_object:
            if entity.parent_index > -1:
                self.can_delete = False
                return context.window_manager.invoke_confirm(operator=self, event=event, message="This entity cannot be removed, since it's parented to another entity.")
            else:
                return context.window_manager.invoke_props_dialog(self, width=300, title="Remove Entity Confirmation")
        return self.execute(context)
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        if self.get_ent(context).linked_object:
            col.prop(self, "delete_obj_from_scene", text=f"Fully remove {self.get_ent(context).linked_object.name} from scene?")

class VICHO_OT_go_to_entity(bpy.types.Operator, YmapData):
    """It zooms in to selected entity in the 3D Viewport"""
    bl_idname = "ymap.go_to_entity"
    bl_label = "Go to entity"
    
    def execute(self, context):
        entity = self.get_ent(context)
        if entity.linked_object:
            bpy.context.view_layer.objects.active = entity.linked_object
            bpy.ops.object.select_all(action='DESELECT')
            entity.linked_object.select_set(True)
            bpy.ops.view3d.view_selected()
        
        return {'FINISHED'}
    
class VICHO_OT_import_entity_sets(bpy.types.Operator, YmapData):
    """Imports entity sets from the entity's MLO archetype definition"""
    bl_idname = "ymap.import_entity_sets"
    bl_label = "Import Entity Sets"
    
    entity_sets: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup) # type: ignore
    
    @classmethod
    def poll(cls, context):
        scene = context.scene
        return len(scene.ymap_list) > 0 and len(scene.ymap_list[scene.ymap_list_index].entities) > 0

    def execute(self, context):
        entity = self.get_ent(context)
        for es in self.entity_sets:
            if es["checked"]:
                if not any(existing_es.name == es.name for existing_es in entity.default_entity_sets):
                    entity.default_entity_sets.add().name = es.name
                else:
                    self.report({'WARNING'}, f"Entity set '{es.name}' already exists in default entity sets")
        context.area.tag_redraw()
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        if len(self.entity_sets) == 0:
            for es in get_entity_sets_from_entity(self, context):
                item = self.entity_sets.add()
                item.name = es
                if not hasattr(item, "checked"):
                    item["checked"] = False

        for item in (self.entity_sets):
            row = layout.row()
            row.prop(item, '["checked"]', text=item.name)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300, title="Import Entity Sets")

class VICHO_OT_remove_entity_set(bpy.types.Operator, YmapData):
    """Removes the selected entity set from the entity's MLO archetype definition"""
    bl_idname = "ymap.remove_entity_set"
    bl_label = "Remove Entity Set"
    
    @classmethod
    def poll(cls, context):
        return len(context.scene.ymap_list[context.scene.ymap_list_index].entities) > 0
    
    def execute(self, context):
        entity = self.get_ent(context)
        if entity.default_entity_sets:
            entity.default_entity_sets.remove(context.scene.default_entity_sets_index)
            context.scene.default_entity_sets_index = max(0, context.scene.default_entity_sets_index - 1)
            self.report({'INFO'}, "Entity set removed")
        else:
            self.report({'WARNING'}, "No entity sets to remove")
        
        return {'FINISHED'}

class VICHO_OT_select_entity_from_viewport(bpy.types.Operator, YmapData):
    """Selects the entity linked to the currently active object in the viewport"""
    bl_idname = "ymap.select_entity_from_viewport"
    bl_label = "Select Entity from Viewport"
    
    @classmethod
    def poll(cls, context):
        return context.active_object.parent.vicho_type != "vicho_ymap_entities"

    def execute(self, context):
        active_object = context.active_object
        if active_object:
            actual_soll = get_soll_parent(active_object)
            entity, e_idx, ymap, y_idx = self.get_ent_from_sel(context, actual_soll)
            if entity and entity.linked_object.sollum_type in COMPAT_SOLL_TYPES:
                self.set_ymap_index(context, y_idx)
                ymap.active_category = "ENTITIES"
                bpy.ops.ymap.map_data_menu(operator_id="ymap.entities_menu")
                self.set_ent_idx(context, e_idx)
                context.view_layer.objects.active = entity.linked_object
                bpy.ops.object.select_all(action='DESELECT')
                entity.linked_object.select_set(True)
                return {'FINISHED'}
        return {'CANCELLED'}
    
def draw_obj_ctx_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(VICHO_OT_select_entity_from_viewport.bl_idname, text="Select Entity in Viewport")
    
def register():
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_obj_ctx_menu)

def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_obj_ctx_menu)