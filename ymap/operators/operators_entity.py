from bpy.types import Object
from bpy.props import BoolProperty, IntProperty
import bpy
from ..helper import YmapMixin, get_entity_sets_from_entity, get_sel_objs_list
from ..constants import COMPAT_SOLL_TYPES
from ...misc.funcs import delete_hierarchy
from ..funcs import get_soll_parent

class VICHO_OT_add_entity(bpy.types.Operator, YmapMixin):
    """Adds a new entity to the YMAP"""
    bl_idname = "ymap.add_entity"
    bl_label = "Creates a new entity"
    
    @classmethod
    def poll(cls, context):
        return cls.get_ymap_count(context) > 0 and cls.get_ymap_obj(context) is not None

    def execute(self, context):
        ymap, ymap_obj, ymap_eg = self.get_ymap(context), self.get_ymap_obj(context), self.get_ymap_ent_group_obj(context)
        ymap.ymap_entity_group_object = ymap_eg
        if ymap_obj:
            new_entity = ymap.entities.add()
            new_entity.name = "New Entity"
            new_entity.flags.total_flags = 1572864
            self.set_ent_idx(context, len(ymap.entities) - 1)
            self.report({'INFO'}, f"Added new entity to {ymap_obj.name} YMAP")
            return {'FINISHED'}

class VICHO_OT_add_entity_from_selection(bpy.types.Operator, YmapMixin):
    """Add(s) selected objects as entities to the YMAP"""
    bl_idname = "ymap.add_sel_objs_as_entity"
    bl_label = "Add entities from selection"
    
    @classmethod
    def poll(cls, context):
        return cls.get_ymap_count(context) > 0 and cls.get_ymap_obj(context) and get_sel_objs_list(context)

    def execute(self, context):
        selected_objs: list[Object] = get_sel_objs_list(context)
        ymap, ymap_obj, ymap_eg = self.get_ymap(context), self.get_ymap_obj(context), self.get_ymap_ent_group_obj(context)
        if ymap_obj:
            added_entities: str = ""
            self.get_ymap(context).ymap_entity_group_object = ymap_eg
            for obj in selected_objs:
                obj.parent = ymap_eg
                new_entity = ymap.entities.add()
                new_entity.linked_object = obj
                new_entity.linked_object.vicho_ymap_parent = ymap_obj
                new_entity.flags.total_flags = 1572864  # Default flags
                new_entity.is_mlo_instance = True if obj.sollum_type == 'sollumz_bound_composite' else False
                self.set_ent_idx(context, len(ymap.entities) - 1)
                added_entities += f"{obj.name}, "
            self.report({'INFO'}, f"Entities added to {ymap_obj.name} YMAP: {added_entities}")
            return {'FINISHED'}

class VICHO_OT_remove_entity(bpy.types.Operator, YmapMixin):
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
    ) # type: ignore
    
    @classmethod
    def poll(cls, context):
        return cls.get_ymap_ent_count(context) > 0
    
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

class VICHO_OT_go_to_entity(bpy.types.Operator, YmapMixin):
    """It zooms in to selected entity in the 3D Viewport"""
    bl_idname = "ymap.go_to_entity"
    bl_label = "Go to entity"
    
    index: IntProperty(default=-1) # type: ignore
    
    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        ent = self.get_ent_by_index(context, self.index)
        lo: Object = ent.linked_object
        zoom_objects = []
        if lo:
            zoom_objects.append(lo)
            if lo.children_recursive:
                zoom_objects.extend([child for child in lo.children_recursive if child.type == 'MESH'])
            [obj.select_set(True) for obj in zoom_objects]
            bpy.ops.view3d.view_selected()
            bpy.ops.object.select_all(action='DESELECT')
            lo.select_set(True)
        return {'FINISHED'}
    
class VICHO_OT_import_entity_sets(bpy.types.Operator, YmapMixin):
    """Imports entity sets from the entity's MLO archetype definition"""
    bl_idname = "ymap.import_entity_sets"
    bl_label = "Import Entity Sets"
    
    entity_sets: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup) # type: ignore
    
    @classmethod
    def poll(cls, context):
        return cls.get_ymap_count(context) > 0 and cls.has_entities(context)

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
            row.label(text="", icon='SNAP_VOLUME')
            row.prop(item, '["checked"]', text=item.name)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300, title="Import Entity Sets")

class VICHO_OT_add_entity_set(bpy.types.Operator, YmapMixin):
    """Adds a new entity set to the entity's MLO archetype definition"""
    bl_idname = "ymap.add_entity_set"
    bl_label = "Add Entity Set"
    
    @classmethod
    def poll(cls, context):
        return cls.has_entities(context)
    
    def execute(self, context):
        entity = self.get_ent(context)
        new_entity_set = entity.default_entity_sets.add()
        new_entity_set.name = "New Entity Set"
        context.scene.default_entity_sets_index = len(entity.default_entity_sets) - 1
        self.report({'INFO'}, "New entity set added")
        return {'FINISHED'}

class VICHO_OT_remove_entity_set(bpy.types.Operator, YmapMixin):
    """Removes the selected entity set from the entity's MLO archetype definition"""
    bl_idname = "ymap.remove_entity_set"
    bl_label = "Remove Entity Set"
    
    @classmethod
    def poll(cls, context):
        return cls.has_entities(context)

    def execute(self, context):
        entity = self.get_ent(context)
        if entity.default_entity_sets:
            entity.default_entity_sets.remove(context.scene.default_entity_sets_index)
            context.scene.default_entity_sets_index = max(0, context.scene.default_entity_sets_index - 1)
            self.report({'INFO'}, "Entity set removed")
        else:
            self.report({'WARNING'}, "No entity sets to remove")
        
        return {'FINISHED'}

class VICHO_OT_select_entity_from_viewport(bpy.types.Operator, YmapMixin):
    """Selects the entity linked to the currently active object in the viewport"""
    bl_idname = "ymap.select_entity_from_viewport"
    bl_label = "Select Entity from Viewport"
    
    @classmethod
    def poll(cls, context):
        return context.active_object.parent and context.active_object.parent.vicho_type != "vicho_ymap_entities"

    def execute(self, context):
        active_obj = context.active_object
        if active_obj:
            soll_parent = get_soll_parent(active_obj)
            entity, e_idx, ymap, y_idx = self.get_ent_from_viewport_select(context, soll_parent)
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

class VICHO_OT_convert_entity_type(bpy.types.Operator, YmapMixin):
    """Converts the selected entity to/from an MLO instance"""
    bl_idname = "ymap.convert_entity_type"
    bl_label = "Convert Entity Type"
    
    @classmethod
    def poll(cls, context):
        return cls.get_ent(context) is not None
    
    def execute(self, context):
        entity = self.get_ent(context)
        entity.is_mlo_instance = not entity.is_mlo_instance
        if entity.is_mlo_instance:
            self.report({'INFO'}, f"Entity {entity.linked_object.name} converted to an MLO instance")
        else:
            self.report({'INFO'}, f"Entity {entity.linked_object.name} converted to an entity")
        return {'FINISHED'}

class VICHO_OT_entity_selection(bpy.types.Operator, YmapMixin):
    """WIP"""
    bl_idname = "ymap.entity_selection"
    bl_label = "Entity Selection"
    
    index: bpy.props.IntProperty(default=0) # type: ignore
    
    shift_pressed: BoolProperty() # type: ignore
    ctrl_pressed: BoolProperty() # type: ignore
    
    first_idx: IntProperty(default=-1) # type: ignore
    last_idx: IntProperty(default=-1) # type: ignore
    
    selection_count: IntProperty(default=0) # type: ignore
    
    def clear_selection (self, context):
        for ent in self.get_ymap(context).entities:
            ent.is_multi_selected = False
            
    def execute(self, context):
        
        ymap = self.get_ymap(context)
        entities = ymap.entities

        if not hasattr(ymap, "selected_entity_index"):
            ymap.selected_entity_index = []
        
        if self.ctrl_pressed:
            if entities[self.index].is_multi_selected:
                entities[self.index].is_multi_selected = False
                self.selection_count -= 1
            else:
                entities[self.index].is_multi_selected = True
                self.selection_count += 1
            
            selected_idx = [i for i, ent in enumerate(entities) if ent.is_multi_selected]
            ymap["selected_entity_index"] = selected_idx
            
            ymap.entity_multi_select = True if self.selection_count > 1 else False
            return {'FINISHED'}
        
        if self.shift_pressed:
            self.last_idx = self.index
            
            if self.first_idx > self.last_idx:
                self.first_idx, self.last_idx = self.last_idx, self.first_idx
                
            for i in range(self.first_idx, self.last_idx + 1):
                entities[i].is_multi_selected = True
                self.selection_count += 1
                
            ymap.entity_multi_select = True
            selected_idx = [i for i, ent in enumerate(entities) if ent.is_multi_selected]
            ymap["selected_entity_index"] = selected_idx
        else:
            ymap.entity_multi_select = False
            self.clear_selection(context)
            self.set_ent_idx(context, self.index)
            self.get_ent(context).is_multi_selected = True
            self.first_idx = self.index
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        self.shift_pressed = event.shift
        self.ctrl_pressed = event.ctrl

        return self.execute(context)
    
class VICHO_OT_select_all_entities(bpy.types.Operator, YmapMixin):
    """Selects all entities in the YMAP"""
    bl_idname = "ymap.select_all_entities"
    bl_label = "Select All Entities"
    
    @classmethod
    def poll(cls, context):
        return cls.get_ymap_ent_count(context) > 0 and context.region and context.region.type == 'UI'
    
    def execute(self, context):
        ymap = self.get_ymap(context)
        entities = ymap.entities
        
        ymap.entity_multi_select = True
        
        for ent in entities:
            ent.is_multi_selected = True
            
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
        return {'FINISHED'}

class VICHO_OT_deselect_all_entities(bpy.types.Operator, YmapMixin):
    """Deselects all entities in the YMAP"""
    bl_idname = "ymap.deselect_all_entities"
    bl_label = "Deselect All Entities"
    
    @classmethod
    def poll(cls, context):
        return cls.get_ymap_ent_count(context) > 0 and context.region and context.region.type == 'UI'
    
    def execute(self, context):
        ymap = self.get_ymap(context)
        entities = ymap.entities
        ymap.entity_multi_select = False
        
        for ent in entities:
            ent.is_multi_selected = False
            
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
        return {'FINISHED'}  

class VICHO_MT_entity_submenu(bpy.types.Menu):
    bl_label = "Vicho's Tools"
    bl_idname = "VICHO_MT_entity_submenu"

    def draw(self, context):
        layout = self.layout
        layout.operator(VICHO_OT_select_entity_from_viewport.bl_idname)

def draw_obj_ctx_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.menu(VICHO_MT_entity_submenu.bl_idname)

def register():
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_obj_ctx_menu)

def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_obj_ctx_menu)