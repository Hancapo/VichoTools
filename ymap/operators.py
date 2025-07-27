import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty
from .funcs import (import_ymap_to_scene, 
                    remove_ymap_from_scene, 
                    create_ymap_empty, sanitize_name, 
                    calc_ymap_flags, set_ymap_extents, 
                    create_ymap_entities_group)
import os
import time
from .helper import str_loaded_count, set_sollumz_export_settings, change_ent_parenting
from bpy.types import Object
from .constants import COMPAT_SOLL_TYPES
from ..vicho_dependencies import dependencies_manager as d


class VICHO_OT_import_ymap(bpy.types.Operator, ImportHelper):
    """Import(s) all the selected YMAP file(s) from a given directory"""
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

class VICHO_OT_export_ymap(bpy.types.Operator):
    """Export(s) all the selected YMAP file(s) to a given directory"""
    bl_idname = "ymap.export_ymap"
    bl_label = "Export YMAP file(s)"
    
    
    export_assets: BoolProperty(
        name="Export Assets",
        default=True,
        description="Whether or not to export assets linked to the YMAP entities",
    )
    
    directory: StringProperty(
        name="Export Directory",
        description="Directory to export YMAP files to",
        subtype='DIR_PATH'
    )
    
    filter_folder: BoolProperty(
        name="Filter Folder",
        default=True,
        options={'HIDDEN'},
    )
    
    @classmethod
    def poll(cls, context):
        return len(context.scene.ymap_list) > 0
    
    def execute(self, context):
        scene = context.scene
        ymap_list = scene.ymap_list
        for i, ymap in enumerate(ymap_list):
            
            ymap_file = d.YmapFile()
            ymap_file.Name = ymap.ymap_object.name
            ymap.flags.total_flags, ymap.content_flags.total_flags = calc_ymap_flags(ymap)
            
            new_map_data = d.CMapData()
            
            set_ymap_extents(ymap, ymap.entities)
            
            new_map_data.flags, new_map_data.contentFlags = ymap.flags.total_flags, ymap.content_flags.total_flags
            
            new_map_data.streamingExtentsMin = d.Vector3(ymap.streaming_extents_min[0], ymap.streaming_extents_min[1], ymap.streaming_extents_min[2])
            new_map_data.streamingExtentsMax = d.Vector3(ymap.streaming_extents_max[0], ymap.streaming_extents_max[1], ymap.streaming_extents_max[2])
            new_map_data.entitiesExtentsMin = d.Vector3(ymap.entities_extents_min[0], ymap.entities_extents_min[1], ymap.entities_extents_min[2])
            new_map_data.entitiesExtentsMax = d.Vector3(ymap.entities_extents_max[0], ymap.entities_extents_max[1], ymap.entities_extents_max[2])
            
            ymap_file._CMapData = new_map_data

            #Build entities
            if ymap.entities:
                for entity in ymap.entities:
                    if entity.linked_object:
                        lo: Object = entity.linked_object
                        if lo.rotation_mode != 'QUATERNION':
                            lo.rotation_mode = 'QUATERNION'
                        ymap_entity_def = d.YmapEntityDef()
                        entity_def = d.CEntityDef()
                        name_meta = d.MetaHash(d.JenkHash.GenHash(sanitize_name(lo.name)))
                        entity_def.archetypeName = name_meta
                        entity_def.position = d.Vector3(lo.location.x, lo.location.y, lo.location.z)
                        entity_def.rotation = d.Vector4(lo.rotation_quaternion.x, lo.rotation_quaternion.y, lo.rotation_quaternion.z, -lo.rotation_quaternion.w if lo.rotation_quaternion.w != 1 else lo.rotation_quaternion.w)
                        entity_def.scaleXY = lo.scale.x
                        entity_def.scaleZ = lo.scale.z
                        entity_def.lodLevel = d.Enum.Parse(d.rage__eLodType, entity.lod_level)
                        entity_def.ambientOcclusionMultiplier = entity.ambient_occlusion_multiplier
                        entity_def.artificialAmbientOcclusion = entity.artificial_ambient_occlusion
                        entity_def.flags = entity.flags.total_flags
                        entity_def.guid = d.UInt32.Parse(entity.guid)
                        entity_def.tintValue = entity.tint_value
                        entity_def.priorityLevel = d.Enum.Parse(d.rage__ePriorityLevel, entity.priority_level)
                        entity_def.lodDist = entity.lod_distance
                        entity_def.childLodDist = entity.child_lod_distance
                        entity_def.numChildren = entity.num_children
                        entity_def.parentIndex = entity.parent_index
                        #TODO MLO Instance Support
                        ymap_entity_def._CEntityDef = entity_def
                        ymap_file.AddEntity(ymap_entity_def)

            d.File.WriteAllBytes(f"{self.directory}/{ymap_file.Name}.ymap", ymap_file.Save())
            if self.export_assets:
                set_sollumz_export_settings()
                link_objs: list[Object] = [obj.linked_object for obj in ymap.entities if obj.linked_object]
                change_ent_parenting(link_objs)
                os.makedirs(self.directory + f"/{ymap.ymap_object.name}_assets", exist_ok=True)
                scene.sollumz_export_path = f"{self.directory}{ymap.ymap_object.name}_assets"
                bpy.ops.sollumz.export_assets(directory=self.directory + f"/{ymap.ymap_object.name}_assets")
                change_ent_parenting(link_objs, do_parent=True)
                
            self.report({'INFO'}, f"YMAP '{ymap_file.Name}' exported successfully")
        #create dir
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "export_assets", text="Export Assets")

class VICHO_OT_remove_ymap(bpy.types.Operator):
    """Removes the selected YMAP from the list"""
    bl_idname = "ymap.remove_ymap"
    bl_label = "Removes a YMAP"
    
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
    """Adds a new YMAP item to the scene/ymap list"""
    bl_idname = "ymap.add_ymap"
    bl_label = "Creates a new YMAP"
    
    def execute(self, context):
        scene = context.scene
        new_ymap = scene.ymap_list.add()
        new_ymap.ymap_object = create_ymap_empty("New YMAP")
        scene.ymap_list_index = len(scene.ymap_list) - 1
        bpy.ops.ymap.map_data_menu(operator_id="ymap.map_data_menu")
        self.report({'INFO'}, f"YMAP added to scene")
        return {'FINISHED'}

class VICHO_OT_add_entity(bpy.types.Operator):
    """Adds a new entity to the YMAP"""
    bl_idname = "ymap.add_entity"
    bl_label = "Creates a new entity"
    
    @classmethod
    def poll(cls, context):
        scene = context.scene
        return len(scene.ymap_list) > 0 and scene.ymap_list[scene.ymap_list_index].ymap_object

    def execute(self, context):
        scene = context.scene
        ymap = scene.ymap_list[scene.ymap_list_index]
        ymap_obj: Object = ymap.ymap_object
        ymap_eg: Object = create_ymap_entities_group(ymap_obj) if not ymap.ymap_entity_group_object else ymap.ymap_entity_group_object
        ymap.ymap_entity_group_object = ymap_eg

        if ymap_obj:
            new_entity = ymap.entities.add()
            new_entity.name = "New Entity"
            new_entity.flags.total_flags = 1572864
            scene.entity_list_index = len(ymap.entities) - 1
            self.report({'INFO'}, f"Added new entity to {ymap_obj.name} YMAP")
            return {'FINISHED'}

class VICHO_OT_add_entity_from_selection(bpy.types.Operator):
    """Add(s) selected objects as entities to the YMAP"""
    bl_idname = "ymap.add_sel_objs_as_entity"
    bl_label = "Add entities from selection"
    
    @classmethod
    def poll(cls, context):
        scene = context.scene
        return len(scene.ymap_list) > 0 and scene.ymap_list[scene.ymap_list_index].ymap_object

    def execute(self, context):
        scene = context.scene
        selected_objs: list[Object] = [obj for obj in bpy.context.selected_objects if obj.type == 'EMPTY' and obj.sollum_type in COMPAT_SOLL_TYPES]
        ymap = scene.ymap_list[scene.ymap_list_index]
        ymap_obj = ymap.ymap_object
        if ymap_obj:
            ymap_eg: Object = create_ymap_entities_group(ymap_obj) if not ymap.ymap_entity_group_object else ymap.ymap_entity_group_object
            added_entities: str = ""
            for obj in selected_objs:
                obj.parent = ymap_eg
                new_entity = scene.ymap_list[scene.ymap_list_index].entities.add()
                new_entity.linked_object = obj
                new_entity.linked_object.vicho_ymap_parent = ymap_obj
                new_entity.flags.total_flags = 1572864  # Default flags
                scene.entity_list_index = len(ymap.entities) - 1
                added_entities += f"{obj.name}, "
            self.report({'INFO'}, f"Entities added to {ymap_obj.name} YMAP: {added_entities}")
            return {'FINISHED'}

class VICHO_OT_remove_entity(bpy.types.Operator):
    """Remove entity from the YMAP"""
    bl_idname = "ymap.remove_entity"
    bl_label = "Remove entity from YMAP"
    
    @classmethod
    def poll(cls, context):
        return len(context.scene.ymap_list) > 0 and len(context.scene.ymap_list[context.scene.ymap_list_index].entities) > 0
    
    def execute(self, context):
        scene = context.scene
        selected_ymap_index = scene.ymap_list_index
        selected_entity_index = scene.entity_list_index
        
        if selected_entity_index >= 0:
            entity = scene.ymap_list[selected_ymap_index].entities[selected_entity_index]
            ymap = scene.ymap_list[selected_ymap_index]
            ymap.entities.remove(selected_entity_index)
            scene.entity_list_index = max(0, selected_entity_index - 1)
            if entity.linked_object:
                self.report({'INFO'}, f"Entity {entity.linked_object.name} removed from YMAP")
            else :
                self.report({'INFO'}, f"Entity removed from YMAP")
        else:
            self.report({'ERROR'}, f"No entity selected to remove")
        
        return {'FINISHED'}            
    
class VICHO_OT_go_to_entity(bpy.types.Operator):
    """It zooms in to selected entity in the 3D Viewport"""
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
    
class VICHO_OT_calculate_ymap_extents(bpy.types.Operator):
    """It calculates the extents of the current YMAP"""
    bl_idname = "ymap.calculate_extents"
    bl_label = "Calculate YMAP extents"
    
    @classmethod
    def poll(cls, context):
        scene = context.scene
        return len(scene.ymap_list) > 0
    
    def execute(self, context):
        scene = context.scene
        selected_ymap_index = scene.ymap_list_index
        ymap = scene.ymap_list[selected_ymap_index]
        
        if ymap.entities:
            set_ymap_extents(ymap, ymap.entities)
            self.report({'INFO'}, f"YMAP extents calculated")
        else:
            self.report({'WARNING'}, f"No entities in YMAP to calculate extents")
        
        return {'FINISHED'}