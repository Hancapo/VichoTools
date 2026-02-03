import bpy
from bpy.props import (BoolProperty, 
                       StringProperty, 
                       CollectionProperty, 
                       PointerProperty, 
                       EnumProperty)
from bpy_extras.io_utils import ImportHelper

from ..ymap_mixin import YmapMixin
from ...shared.helper import (str_loaded_count, 
                      set_sollumz_export_settings,
                      set_sollumz_import_settings,
                      set_sollumz_export_format_to_binary,
                      set_sollumz_gen_ver,
                      get_meta_hash)
from bpy.types import Object
from ...vicho_dependencies import dependencies_manager as d
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from CodeWalker.GameFiles import (YmapFile,  # type: ignore
                                      CMapData, 
                                      MloArchetype, 
                                      CMloInstanceDef, 
                                      YmapEntityDef, 
                                      MetaHash, 
                                      CEntityDef, 
                                      MloInstanceData)
import time
import os
from ..helper import (import_ymap_to_scene,
                     remove_ymap_from_scene,
                     create_ymap_empty,
                     calc_ymap_flags,
                     set_ymap_ent_extents,
                     set_ymap_strm_extents,
                     change_ymap_ent_parenting)

from ...shared.funcs import sanitize_name
from .operators import VICHO_OT_open_folder
from ...shared.constants import GAME_VERSIONS

class ImportSettings(bpy.types.PropertyGroup):
    import_entities: BoolProperty(name="Entities", default=True, description="Import entities from the YMAP file(s)") # type: ignore
    import_occluders: BoolProperty(name="Occluders", default=True, description="Import occluders including box and model occluders from the YMAP file(s)") # type: ignore
    import_extensions: BoolProperty(name="Entity Extensions", default=True, description="Import entity extensions from the YMAP file(s)") # type: ignore
    import_timecycle_mods: BoolProperty(name="Timecycle Modifiers", default=True, description="Import timecycle modifiers from the YMAP file(s)") # type: ignore
    import_car_generators: BoolProperty(name="Car Generators", default=True, description="Import car generators from the YMAP file(s)") # type: ignore
    import_props: BoolProperty(name="Import Props", default=True, description="Whether or not to import props from the YMAP file(s)") # type: ignore
    remove_cols: BoolProperty(name="Remove Collision", default=False, description="Whether or not to remove collision from imported props") # type: ignore
    remove_lights: BoolProperty(name="Remove Lights", default=False, description="Whether or not to remove lights from imported props") # type: ignore
    remove_non_high: BoolProperty(name="Remove Non-High LOD", default=False, description="Whether or not to remove non-high LOD from imported props") # type: ignore

class VICHO_OT_import_ymap(bpy.types.Operator, ImportHelper):
    """Import(s) all the selected YMAP file(s) from a given directory"""
    bl_idname = "ymap.import_ymap"
    bl_label = "Import YMAP file(s)"

    filename_ext = ".ymap"
    
    filter_glob: StringProperty(
        default="*.ymap",
        options={"HIDDEN"}
    ) # type: ignore
    
    import_settings: PointerProperty(type=ImportSettings) # type: ignore
    
    files: CollectionProperty(type=bpy.types.OperatorFileListElement) # type: ignore
    
    directory: StringProperty(maxlen=1024, default="", subtype='DIR_PATH') # type: ignore
    
    @classmethod
    def poll(cls, context):
        return str_loaded_count() > 0

    def execute(self, context):
        scene = context.scene
        start_time = time.time()
        set_sollumz_import_settings()
        for file in self.files:
            filepath: str = os.path.join(self.directory, file.name)
            import_ymap_to_scene(scene, filepath, self.import_settings, self, scene.ymap_assets_path)
        self.report({'INFO'}, f"YMAP file(s) imported in {time.time() - start_time:.2f} seconds")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.use_property_decorate = False
        layout.use_property_split = True
        
        header, body = layout.panel("YMAP_import", default_closed=False)
        header.label(text="Import Settings")
        if body:
            sublayout = body.column(heading="Include")
            sublayout.prop(self.import_settings, "import_entities", text="Entities")
            sublayout.prop(self.import_settings, "import_occluders", text="Occluders")
            sublayout.prop(self.import_settings, "import_extensions", text="Entity Extensions")
            sublayout.prop(self.import_settings, "import_timecycle_mods", text="Timecycle Modifiers")
            sublayout.prop(self.import_settings, "import_car_generators", text="Car Generators")
            if self.import_settings.import_entities:
                sublayout.separator(type="LINE")
                sublayout.prop(scene, "ymap_assets_path", text="Assets Path")
                sublayout = body.row()
                sublayout.operator(VICHO_OT_open_folder.bl_idname, text="Open Assets Folder", icon='FILE_FOLDER')
        
        if self.import_settings.import_entities:
            header, body = layout.panel("YMAP_purify", default_closed=True) 
            header.label(text="Purify Settings")
            
            if body:
                sublayout = body.column(heading="Remove")
                sublayout.prop(self.import_settings, "remove_cols", text="Collisions")
                sublayout.prop(self.import_settings, "remove_lights", text="Lights")
                sublayout.prop(self.import_settings, "remove_non_high", text="Non-High LOD")

class VICHO_OT_export_ymap(bpy.types.Operator, YmapMixin):
    """Export(s) all the selected YMAP file(s) to a given directory"""
    bl_idname = "ymap.export_ymap"
    bl_label = "Export YMAP file(s)"
    
    
    export_assets: BoolProperty(
        name="Export Assets",
        default=False,
        description="Whether or not to export assets linked to the YMAP entities",
    ) # type: ignore
     
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
        items=GAME_VERSIONS,
        options={'ENUM_FLAG'},
        default=set(['Legacy']),
    ) # type: ignore

    calc_strm_extents: BoolProperty(name="Calculate Streaming Extents", default=True) # type: ignore
    calc_ent_extents: BoolProperty(name="Calculate Entities Extents", default=True) # type: ignore

    calc_flags: BoolProperty(name="Calculate Flags", default=True) # type: ignore
    calc_content_flags: BoolProperty(name="Calculate Content Flags", default=True) # type: ignore

    @classmethod
    def poll(cls, context):
        return len(context.scene.ymap_list) > 0 and any(ymap for ymap in context.scene.ymap_list if ymap.enabled)

    def execute(self, context):
        scene = context.scene
        ymap_list = [ymap for ymap in scene.ymap_list if ymap.enabled]
        for i, ymap in enumerate(ymap_list):
            if self.calc_flags:
                ymap.flags.total_flags, _ = calc_ymap_flags(ymap)
            if self.calc_content_flags:
                _, ymap.content_flags.total_flags = calc_ymap_flags(ymap)
            if self.calc_strm_extents:
                set_ymap_strm_extents(ymap, ymap.entities)
            
            if self.calc_ent_extents:
                set_ymap_ent_extents(ymap, ymap.entities)
                
            ymap_file: "YmapFile" = d.YmapFile()
            ymap_file.Name = ymap.ymap_object.name
            new_cmapdata: "CMapData" = d.CMapData()
            
            new_cmapdata.parent = get_meta_hash(ymap.parent)
            
            new_cmapdata.flags, new_cmapdata.contentFlags = ymap.flags.total_flags, ymap.content_flags.total_flags
            new_cmapdata.streamingExtentsMin = d.Vector3(ymap.streaming_extents_min[0], ymap.streaming_extents_min[1], ymap.streaming_extents_min[2])
            new_cmapdata.streamingExtentsMax = d.Vector3(ymap.streaming_extents_max[0], ymap.streaming_extents_max[1], ymap.streaming_extents_max[2])
            new_cmapdata.entitiesExtentsMin = d.Vector3(ymap.entities_extents_min[0], ymap.entities_extents_min[1], ymap.entities_extents_min[2])
            new_cmapdata.entitiesExtentsMax = d.Vector3(ymap.entities_extents_max[0], ymap.entities_extents_max[1], ymap.entities_extents_max[2])
            
            ymap_file._CMapData = new_cmapdata

            if ymap.ymap_phys_dicts:
                phys_dicts: list["MetaHash"] = []
                for phys_dict in ymap.ymap_phys_dicts:
                    phys_dicts.append(get_meta_hash(phys_dict.name))
                ymap_file.physicsDictionaries = phys_dicts
            #Build entities
            if ymap.entities:
                for entity in ymap.entities:
                    if entity.linked_object:
                        lo: Object = entity.linked_object
                        if lo.rotation_mode != 'QUATERNION':
                            lo.rotation_mode = 'QUATERNION'
                        ymap_entity_def: "YmapEntityDef" = d.YmapEntityDef()
                        ent_def: "CEntityDef" = d.CEntityDef()
                        name_meta: "MetaHash" = d.MetaHash(d.JenkHash.GenHash(sanitize_name(lo.name)))
                        ent_def.archetypeName = name_meta
                        ent_def.position = d.Vector3(lo.location.x, lo.location.y, lo.location.z)
                        ent_def.rotation = d.Vector4(lo.rotation_quaternion.x, lo.rotation_quaternion.y, 
                                                     -lo.rotation_quaternion.z if entity.is_mlo_instance else lo.rotation_quaternion.z, 
                                                     -lo.rotation_quaternion.w if lo.rotation_quaternion.w != 1 else lo.rotation_quaternion.w)
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
                            mlo_arch: "MloArchetype" = d.MloArchetype()
                            mlo_inst_data: "MloInstanceData" = d.MloInstanceData(ymap_entity_def, mlo_arch)
                            if entity.default_entity_sets:
                                mlo_inst_data.defaultEntitySets = [get_meta_hash(des.name) for des in entity.default_entity_sets]
                            cmlo_inst: "CMloInstanceDef" = d.CMloInstanceDef()
                            cmlo_inst.groupId = entity.group_id
                            cmlo_inst.floorId = entity.floor_id
                            cmlo_inst.MLOInstflags = entity.mlo_inst_flags
                            cmlo_inst.numExitPortals = entity.num_exit_portals
                            
                            ymap_entity_def.MloInstance = mlo_inst_data
                            ymap_entity_def.MloInstance.Instance = cmlo_inst

                        ymap_entity_def.CEntityDef = ent_def
                        ymap_file.AddEntity(ymap_entity_def)

            d.File.WriteAllBytes(f"{self.directory}/{ymap_file.Name}.ymap", ymap_file.Save())
            if self.export_assets:
                set_sollumz_export_settings()
                set_sollumz_export_format_to_binary()
                set_sollumz_gen_ver(self.version)
                link_objs: list[Object] = [obj.linked_object for obj in ymap.entities if obj.linked_object and '.' not in obj.linked_object.name]
                change_ymap_ent_parenting(link_objs)
                ymap_asset_folder = f"/{ymap.ymap_object.name}_assets"
                os.makedirs(self.directory + ymap_asset_folder, exist_ok=True)
                bpy.ops.sollumz.export_assets(directory=self.directory + f'/{ymap_asset_folder}' )
                change_ymap_ent_parenting(link_objs, do_parent=True)
            self.report({'INFO'}, f"YMAP '{ymap_file.Name}' exported successfully")
        #create dir
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        header, body = layout.panel("YMAP_calc", default_closed=False)
        header.label(text="Calculate")
        if body:
            sublayout = body.column()
            sublayout.prop(self, "calc_strm_extents", text="Streaming Extents")
            sublayout.prop(self, "calc_ent_extents", text="Entities Extents")
            sublayout.prop(self, "calc_flags", text="Flags")
            sublayout.prop(self, "calc_content_flags", text="Content Flags")
        layout.use_property_split = False
        header, body = layout.panel("YMAP_export_assets", default_closed=False)
        header.prop(self, "export_assets", text="Export Assets")
        if body:
            body.enabled = self.export_assets
            split = body.split(factor=0.35)
            left = split.column()
            right = split.column(align=True)
            left.label(text="Game Version")
            right.use_property_split = False
            right.prop_enum(self, "version", 'Legacy',   icon='EVENT_NDOF_BUTTON_8')
            right.prop_enum(self, "version", 'Enhanced', icon='EVENT_NDOF_BUTTON_9')


class VICHO_OT_remove_ymap(bpy.types.Operator, YmapMixin):
    """Removes the selected YMAP from the list"""
    bl_idname = "ymap.remove_ymap"
    bl_label = "Removes a YMAP"
    
    delete_hierarchy_from_scene: BoolProperty(
        name="Delete Hierarchy from Scene",
        default=False,
        description="Whether to delete the YMAP hierarchy (Everything) from the scene when removing the YMAP",
    ) # type: ignore

    @classmethod
    def poll(cls, context):
        return context.scene.ymap_list_index >= 0 and len(context.scene.ymap_list) > 0
    
    def execute(self, context):
        scene = context.scene
        selected_ymap_index = scene.ymap_list_index
        if remove_ymap_from_scene(scene, selected_ymap_index, self.delete_hierarchy_from_scene):
            scene.ymap_list.remove(selected_ymap_index)
            if len(scene.ymap_list) > 0:
                scene.ymap_list_index = max(0, selected_ymap_index - 1)
            self.report({'INFO'}, "YMAP removed from scene")
        else:
            self.report({'ERROR'}, "Error removing YMAP from scene")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=600, title="YMAP removal confirmation")

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        if self.get_ymap(context).ymap_object:
            col.prop(self, "delete_hierarchy_from_scene", text=f"Delete {self.get_ymap(context).ymap_object.name} entities?")
    
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
    
class VICHO_OT_calculate_ymap_extents(bpy.types.Operator, YmapMixin):
    """Calculates current YMAP's streaming and entities extents"""
    bl_idname = "ymap.calculate_extents"
    bl_label = "Calculate YMAP extents"
    
    @classmethod
    def poll(cls, context):
        return cls.has_entities(context)
    
    def execute(self, context):
        ymap = self.get_ymap(context)
        set_ymap_ent_extents(ymap, ymap.entities)
        set_ymap_strm_extents(ymap, ymap.entities)
        self.report({'INFO'}, f"{ymap.ymap_object.name} extents calculated")

        return {'FINISHED'}
    
class VICHO_OT_calculate_ymap_flags(bpy.types.Operator, YmapMixin):
    """Calculates current YMAP's flags"""
    
    bl_idname = "ymap.calculate_flags"
    bl_label = "Calculate YMAP flags"
    
    @classmethod
    def poll(cls, context):
        return cls.has_entities(context)
    
    def execute(self, context):
        ymap = self.get_ymap(context)
        ymap.flags.total_flags, ymap.content_flags.total_flags = calc_ymap_flags(ymap)
        self.report({'INFO'}, f"{ymap.ymap_object.name} flags calculated")
        return {'FINISHED'}