from bpy.types import Object
from bpy.props import BoolProperty, IntProperty, StringProperty, EnumProperty
import bpy
from ..helper import (YmapMixin, get_entity_sets_from_entity, 
                      get_sel_objs_list, change_ent_parenting, 
                      set_sollumz_export_settings,
                      set_sollumz_export_format_to_binary,
                      set_sollumz_gen_ver)
from ..constants import COMPAT_SOLL_TYPES
from ...misc.funcs import delete_hierarchy
from ..funcs import get_soll_parent, sanitize_name
import os

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
                new_entity.archetype_name = sanitize_name(obj.name)
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
    
    def delete_ent(self, context, entity, ymap):
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

    def reset_selection(self, context):
        scene = context.scene
        selected_entity_index = scene.entity_list_index
        scene.entity_list_index = max(0, selected_entity_index - 1)

    
    def execute(self, context):
        ymap, entity = self.get_ymap(context), self.get_ent(context)
        if self.can_delete:
            if ymap.entity_multi_select:
                ents_indices: list[int] = [i for i, ent in enumerate(ymap.entities) if ent.is_multi_selected]
                deleted_count: int = len(ents_indices)
                for i in sorted(ents_indices, reverse=True):
                    ent = ymap.entities[i]
                    self.delete_ent(context, ent, ymap)
                    ymap.entities.remove(i)

                self.reset_selection(context)
                self.report({'INFO'}, f"Removed {deleted_count} entities from {ymap.ymap_object.name} YMAP")
                return {'FINISHED'}
            
            else:
                self.delete_ent(context, entity, ymap)
                ymap.entities.remove(context.scene.entity_list_index)
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
        ymap = self.get_ymap(context)
        layout = self.layout
        col = layout.column()
        col.label(text="Are you sure you want to remove the selected entities?")
        col.prop(self, "delete_obj_from_scene", text="Fully remove from scene.")
        if ymap.entity_multi_select:
            selected_ents = [ent for ent in self.get_ymap(context).entities if ent.is_multi_selected]
            for ent in selected_ents:
                row = col.row()
                row.label(text=f"- {ent.linked_object.name if ent.linked_object else 'Unnamed Entity'}")
        else:
            if self.get_ent(context).linked_object:
                col.label(text=self.get_ent(context).linked_object.name)

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
            for es in get_entity_sets_from_entity(context):
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
    """Entity Selection"""
    bl_idname = "ymap.entity_selection"
    bl_label = "Entity Selection"
    
    index: bpy.props.IntProperty(default=0) # type: ignore
    
    shift_pressed: BoolProperty() # type: ignore
    ctrl_pressed: BoolProperty() # type: ignore
    
    first_idx: IntProperty(default=-1) # type: ignore
    last_idx: IntProperty(default=-1) # type: ignore
    
    selection_count: IntProperty(default=0) # type: ignore
    
    filter_string: bpy.props.StringProperty(default="") # type: ignore
            
    def execute(self, context):
        
        ymap = self.get_ymap(context)
        entities = ymap.entities
        filtered_entities: list[int] = self.get_filtered_entities_idx(context, self.filter_string)
        
        if not hasattr(ymap, "selected_entity_index"):
            ymap.selected_entity_index = []
        
        if self.ctrl_pressed:
            if entities[self.index].is_multi_selected:
                entities[self.index].is_multi_selected = False
                self.selection_count -= 1
            else:
                entities[self.index].is_multi_selected = True
                self.selection_count += 1
            
            selected_idx: list[int] = [i for i, ent in enumerate(entities) if ent.is_multi_selected]
            ymap["selected_entity_index"] = selected_idx
            
            ymap.entity_multi_select = True if self.selection_count > 1 else False
            return {'FINISHED'}
        
        if self.shift_pressed:
            self.last_idx = self.index
            
            if self.first_idx > self.last_idx:
                self.first_idx, self.last_idx = self.last_idx, self.first_idx
            
            indices = range(self.first_idx, self.last_idx + 1)
            for i in indices:
                if self.filter_string == "" or i in filtered_entities:
                    entities[i].is_multi_selected = True
                    self.selection_count += 1
                
            ymap.entity_multi_select = True
            selected_idx: list[int] = [i for i, ent in enumerate(entities) if ent.is_multi_selected]
            ymap["selected_entity_index"] = selected_idx
        else:
            ymap.entity_multi_select = False
            YmapMixin.clear_entities_selection(context)
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
    
    filter_string: bpy.props.StringProperty(default="") # type: ignore
    
    @classmethod
    def poll(cls, context):
        return cls.get_ymap_ent_count(context) > 0 and context.region and context.region.type == 'UI'
    
    def execute(self, context):
        ymap = self.get_ymap(context)
        ymap.entity_multi_select = True
        ymap["selected_entity_index"] = [ent_idx for ent_idx in range(len(ymap.entities))]
        for ent in enumerate(ymap.entities):
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

class VICHO_OT_export_entity_asset(bpy.types.Operator, YmapMixin):
    """Exports the selected entity's linked object as a Sollumz asset"""
    bl_idname = "ymap.export_entity_asset"
    bl_label = "Export Entity Asset"
    
    directory: StringProperty(
        name="Export Directory",
        description="Directory to export YMAP files to",
        subtype='DIR_PATH'
    ) # type: ignore
    
    filter_folder: BoolProperty(
        name="Filter Folder",
        default=True,
        options={'HIDDEN'},
    ) # type: ignore

    version: EnumProperty(
        name="Game Version",
        description="Select the game version for the exported asset",
        items=[
            ('Legacy', "Legacy", "Export asset for GTA V Legacy"),
            ('Enhanced', "Enhanced", "Export asset for GTA V Enhanced Edition"),
        ],
        options={'ENUM_FLAG'},
        default=set({'Enhanced'}),

    ) # type: ignore

    export_inside_ymap_folder: BoolProperty(
        name="Export Inside YMAP Folder",
        default=True,
        description="Export assets inside a folder named after the YMAP",
    ) # type: ignore

    def export_ent_asset(self, ymap, entity) -> bool:
        lo: Object = entity.linked_object
        if lo and lo.sollum_type in COMPAT_SOLL_TYPES:
            change_ent_parenting([lo])
            final_folder = self.directory + f"/{ymap.ymap_object.name}_assets" if self.export_inside_ymap_folder else self.directory
            os.makedirs(final_folder, exist_ok=True)
            set_sollumz_export_format_to_binary()
            print(self.version)
            set_sollumz_gen_ver(self.version)
            bpy.ops.sollumz.export_assets(directory=final_folder)
            change_ent_parenting([lo], do_parent=True)
            return True
        
    @classmethod
    def poll(cls, context):
        ent = cls.get_ent(context)
        return ent.linked_object is not None
    
    def execute(self, context):
        set_sollumz_export_settings()
        entity = self.get_ent(context)
        ymap = self.get_ymap(context)
        if ymap.entity_multi_select:
            selected_ents = [ent for ent in ymap.entities if ent.is_multi_selected]
            exported_count: int = len(selected_ents)
            for ent in selected_ents:
                if not self.export_ent_asset(ymap, ent):
                    self.report({'ERROR'}, f"Failed to export asset for entity {ent.linked_object.name}")
            self.report({'INFO'}, f"Exported assets for {exported_count} entities.")
        else:
            if self.export_ent_asset(ymap, entity):
                self.report({'INFO'}, f"Exported asset for entity {entity.linked_object.name}")
            else:
                self.report({'ERROR'}, "Failed to export asset.")
                return {'CANCELLED'}
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        ymap = self.get_ymap(context)

        col.prop(self, "export_inside_ymap_folder")
        col = layout.column(align=True)

        for f in {'Legacy', 'Enhanced'}:
            col.prop_enum(self, "version", f)
        
        if ymap.entity_multi_select:
            selected_ents = [ent for ent in ymap.entities if ent.is_multi_selected]
            export_count: int = len(selected_ents)
            col.label(text=f"Exporting {export_count} entities:")
            for ent in selected_ents:
                row = layout.row()
                row.label(text=f"- {sanitize_name(ent.linked_object.name)}")
        else:
            entity = self.get_ent(context)
            layout.label(text=f"Exporting: {sanitize_name(entity.linked_object.name)}")
            col = layout.column(align=True)
            
        

def draw_obj_ctx_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.menu(VICHO_MT_entity_submenu.bl_idname)

def register():
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_obj_ctx_menu)

def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_obj_ctx_menu)