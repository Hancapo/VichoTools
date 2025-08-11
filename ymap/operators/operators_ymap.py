import bpy
from bpy.props import BoolProperty, StringProperty
from bpy_extras.io_utils import ImportHelper
from ..helper import str_loaded_count, set_sollumz_export_settings, change_ent_parenting, YmapData
from bpy.types import Object
from ...vicho_dependencies import dependencies_manager as d
import time
import os
from ..funcs import import_ymap_to_scene, remove_ymap_from_scene, create_ymap_empty, sanitize_name, calc_ymap_flags, set_ymap_extents
from .operators import VICHO_OT_open_folder
from ...misc.funcs import get_meta_hash

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
    
    import_props: BoolProperty(name="Import Props", default=True, description="Whether or not to import props from the YMAP file(s)")
    
    @classmethod
    def poll(cls, context):
        return str_loaded_count() > 0

    def execute(self, context):
        scene = context.scene
        start_time = time.time()
        
        for file in self.files:
            filepath: str = os.path.join(self.directory, file.name)
            import_ymap_to_scene(scene, filepath, self.import_entities, self.import_occluders, self.import_timecycle_mods, self.import_car_generators, self.import_props, self, scene.ymap_assets_path)
        self.report({'INFO'}, f"YMAP file(s) imported in {time.time() - start_time:.2f} seconds")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def draw(self, context):
        scene = context.scene
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
                row = col.row(align=True)
                row.prop(scene, "ymap_assets_path")
                row.operator(VICHO_OT_open_folder.bl_idname, text="", icon='FILE_FOLDER')
                col.separator()
                col.prop(self, "import_props")

class VICHO_OT_export_ymap(bpy.types.Operator):
    """Export(s) all the selected YMAP file(s) to a given directory"""
    bl_idname = "ymap.export_ymap"
    bl_label = "Export YMAP file(s)"
    
    
    export_assets: BoolProperty(
        name="Export Assets",
        default=False,
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
            if ymap.ymap_phys_dicts:
                phys_dicts = []
                for phys_dict in ymap.ymap_phys_dicts:
                    phys_dicts.append(get_meta_hash(phys_dict.name))
                ymap_file.physicsDictionaries = phys_dicts
            if ymap.entities:
                for entity in ymap.entities:
                    if entity.linked_object:
                        lo: Object = entity.linked_object
                        if lo.rotation_mode != 'QUATERNION':
                            lo.rotation_mode = 'QUATERNION'
                        ymap_entity_def = d.YmapEntityDef()
                        ent_def = d.CEntityDef()
                        name_meta = d.MetaHash(d.JenkHash.GenHash(sanitize_name(lo.name)))
                        ent_def.archetypeName = name_meta
                        ent_def.position = d.Vector3(lo.location.x, lo.location.y, lo.location.z)
                        ent_def.rotation = d.Vector4(lo.rotation_quaternion.x, lo.rotation_quaternion.y, lo.rotation_quaternion.z, -lo.rotation_quaternion.w if lo.rotation_quaternion.w != 1 else lo.rotation_quaternion.w)
                        ent_def.scaleXY = lo.scale.x
                        ent_def.scaleZ = lo.scale.z
                        ent_def.lodLevel = d.Enum.Parse(d.rage__eLodType, entity.lod_level)
                        ent_def.ambientOcclusionMultiplier = entity.ambient_occlusion_multiplier
                        ent_def.artificialAmbientOcclusion = entity.artificial_ambient_occlusion
                        ent_def.flags = entity.flags.total_flags
                        ent_def.guid = d.UInt32.Parse(entity.guid)
                        ent_def.tintValue = entity.tint_value
                        ent_def.priorityLevel = d.Enum.Parse(d.rage__ePriorityLevel, entity.priority_level)
                        ent_def.lodDist = entity.lod_distance
                        ent_def.childLodDist = entity.child_lod_distance
                        ent_def.numChildren = entity.num_children
                        ent_def.parentIndex = entity.parent_index
                        
                        if entity.is_mlo_instance:
                            mlo_arch = d.MloArchetype()
                            mlo_inst_data = d.MloInstanceData(ymap_entity_def, mlo_arch)
                            if entity.default_entity_sets:
                                mlo_inst_data.defaultEntitySets = [get_meta_hash(des.name) for des in entity.default_entity_sets]
                            cmlo_inst = d.CMloInstanceDef()
                            cmlo_inst.groupId = entity.group_id
                            cmlo_inst.floorId = entity.floor_id
                            cmlo_inst.MLOInstflags = entity.mlo_inst_flags
                            cmlo_inst.numExitPortals = entity.num_exit_portals
                            
                            ymap_entity_def.MloInstance = mlo_inst_data
                            ymap_entity_def.MloInstance.Instance = cmlo_inst

                        ymap_entity_def._CEntityDef = ent_def
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
            self.report({'INFO'}, "YMAP removed from scene")
        else:
            self.report({'ERROR'}, "Error removing YMAP from scene")
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
        self.report({'INFO'}, "YMAP added to scene")
        return {'FINISHED'}
    
class VICHO_OT_calculate_ymap_extents(bpy.types.Operator, YmapData):
    """It calculates the extents of the current YMAP"""
    bl_idname = "ymap.calculate_extents"
    bl_label = "Calculate YMAP extents"
    
    @classmethod
    def poll(cls, context):
        scene = context.scene
        return len(scene.ymap_list) > 0
    
    def execute(self, context):
        ymap = self.get_ymap(context)
        if ymap.entities:
            set_ymap_extents(ymap, ymap.entities)
            self.report({'INFO'}, f"{ymap.name} extents calculated")
        else:
            self.report({'WARNING'}, f"No entities in {ymap.name} to calculate extents")

        return {'FINISHED'}