import bpy
from .constants import (LOD_LEVELS,
                        ENTITY_TYPES, 
                        YMAP_MAP_DATA_TOGGLES, 
                        ENTITY_TOGGLES, 
                        PRIORITY_LEVELS)

from .helper import (update_entity_flags_bool_properties, 
                     update_entity_flags, 
                     update_ymap_flags_bool_properties, 
                     update_ymap_flags, 
                     update_ymap_content_flags_bool_properties, 
                     update_ymap_content_flags,
                     update_entity_index)


class PhysicsGroup(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Name",
        default="my_physics_group",
        description="Name of the physics group",
        maxlen=60,
    ) # type: ignore
 
class EntityFlags(bpy.types.PropertyGroup):
    total_flags: bpy.props.IntProperty(
        name="Flags",
        default=0,
        min=0,
        description="Entity flags",
        update=update_entity_flags_bool_properties) # type: ignore
    allow_full_rotation: bpy.props.BoolProperty(
        name="Allow Full Rotation",
        default=False,
        description="Allow Full Rotation",
        update=update_entity_flags) # type: ignore
    
    stream_low_priority: bpy.props.BoolProperty(
        name="Stream Low Priority",
        default=False,
        description="Stream Low Priority",
        update=update_entity_flags) # type: ignore
    
    disable_embedded_collision: bpy.props.BoolProperty(
        name="Disable Embedded Collision",
        default=False,
        description="Disable Embedded Collision",
        update=update_entity_flags) # type: ignore
    
    lod_in_parent_map: bpy.props.BoolProperty(
        name="LOD In Parent Map",
        default=False,
        description="LOD In Parent Map",
        update=update_entity_flags) # type: ignore
    
    lod_adopt_me: bpy.props.BoolProperty(
        name="LOD Adopt Me",
        default=False,
        description="LOD Adopt Me",
        update=update_entity_flags) # type: ignore
    
    static_entity: bpy.props.BoolProperty(
        name="Static Entity",
        default=False,
        description="Static Entity",
        update=update_entity_flags) # type: ignore
    
    interior_lod: bpy.props.BoolProperty(
        name="Interior LOD",
        default=False,
        description="Interior LOD",
        update=update_entity_flags) # type: ignore
    
    lod_use_alt_fade: bpy.props.BoolProperty(
        name="LOD Use Alt Fade",
        default=False,
        description="LOD Use Alt Fade",
        update=update_entity_flags) # type: ignore
    
    underwater: bpy.props.BoolProperty(
        name="Underwater",
        default=False,
        description="Underwater",
        update=update_entity_flags) # type: ignore
    
    doesnt_touch_water: bpy.props.BoolProperty(
        name="Doesn't Touch Water",
        default=False,
        description="Doesn't Touch Water",
        update=update_entity_flags) # type: ignore
    
    doesnt_spawn_peds: bpy.props.BoolProperty(
        name="Doesn't Spawn Peds",
        default=False,
        description="Doesn't Spawn Peds",
        update=update_entity_flags) # type: ignore
    
    cast_static_shadows: bpy.props.BoolProperty(
        name="Cast Static Shadows",
        default=False,
        description="Cast Static Shadows",
        update=update_entity_flags) # type: ignore
    
    cast_dynamic_shadows: bpy.props.BoolProperty(
        name="Cast Dynamic Shadows",
        default=False,
        description="Cast Dynamic Shadows",
        update=update_entity_flags) # type: ignore
    
    ignore_time_settings: bpy.props.BoolProperty(
        name="Ignore Time Settings",
        default=False,
        description="Ignore Time Settings",
        update=update_entity_flags) # type: ignore
    
    dont_render_shadows: bpy.props.BoolProperty(
        name="Don't Render Shadows",
        default=False,
        description="Don't Render Shadows",
        update=update_entity_flags) # type: ignore
    
    only_render_shadows: bpy.props.BoolProperty(
        name="Only Render Shadows",
        default=False,
        description="Only Render Shadows",
        update=update_entity_flags) # type: ignore
    
    dont_render_reflections: bpy.props.BoolProperty(
        name="Don't Render Reflections",
        default=False,
        description="Don't Render Reflections",
        update=update_entity_flags)  # type: ignore
    
    only_render_reflections: bpy.props.BoolProperty(
        name="Only Render Reflections",
        default=False,
        description="Only Render Reflections",
        update=update_entity_flags)  # type: ignore
    
    dont_render_water_reflections: bpy.props.BoolProperty(
        name="Don't Render Water Reflections",
        default=False,
        description="Don't Render Water Reflections",
        update=update_entity_flags) # type: ignore
    
    only_render_water_reflections: bpy.props.BoolProperty(
        name="Only Render Water Reflections",
        default=False,
        description="Only Render Water Reflections",
        update=update_entity_flags) # type: ignore
    
    dont_render_mirror_reflections: bpy.props.BoolProperty(
        name="Don't Render Mirror Reflections",
        default=False,
        description="Don't Render Mirror Reflections",
        update=update_entity_flags) # type: ignore
    
    only_render_mirror_reflections: bpy.props.BoolProperty(
        name="Only Render Mirror Reflections",
        default=False,
        description="Only Render Mirror Reflections",
        update=update_entity_flags) # type: ignore

class EntitySetsProps(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Name",
        default="",
        description="Name",
        maxlen=60) # type: ignore

class YmapMapDataContentFlags(bpy.types.PropertyGroup):
    total_flags: bpy.props.IntProperty(
        name="Flags",
        default=0,
        min=0,
        description="YMAP flags",
        update=update_ymap_content_flags_bool_properties) # type: ignore
    hd: bpy.props.BoolProperty(
        name="HD",
        default=False,
        description="HD",
        update=update_ymap_content_flags) # type: ignore
    
    lod: bpy.props.BoolProperty(
        name="LOD",
        default=False,
        description="LOD",
        update=update_ymap_content_flags) # type: ignore
    
    slod2_plus: bpy.props.BoolProperty(
        name="SLOD2+",
        default=False,
        description="SLOD2+",
        update=update_ymap_content_flags) # type: ignore
    
    interior: bpy.props.BoolProperty(
        name="Interior",
        default=False,
        description="Interior",
        update=update_ymap_content_flags) # type: ignore
    
    slod: bpy.props.BoolProperty(
        name="SLOD",
        default=False,
        description="SLOD",
        update=update_ymap_content_flags) # type: ignore
    
    occlusion: bpy.props.BoolProperty(
        name="Occlusion",
        default=False,
        description="Occlusion",
        update=update_ymap_content_flags) # type: ignore
    
    physics: bpy.props.BoolProperty(
        name="Physics",
        default=False,
        description="Physics",
        update=update_ymap_content_flags) # type: ignore
    
    lod_lights: bpy.props.BoolProperty(
        name="LOD Lights",
        default=False,
        description="LOD Lights",
        update=update_ymap_content_flags) # type: ignore
    
    distant_lights: bpy.props.BoolProperty(
        name="Distant Lights",
        default=False,
        description="Distant Lights",
        update=update_ymap_content_flags) # type: ignore
    
    critical: bpy.props.BoolProperty(
        name="Critical",
        default=False,
        description="Critical",
        update=update_ymap_content_flags) # type: ignore
    
    grass: bpy.props.BoolProperty(
        name="Grass",
        default=False,
        description="Grass",
        update=update_ymap_content_flags) # type: ignore

class YmapMapDataFlags(bpy.types.PropertyGroup):
    total_flags: bpy.props.IntProperty(
        name="Flags",
        default=0,
        min=0,
        description="YMAP content flags",
        update=update_ymap_flags_bool_properties) # type: ignore
    
    script: bpy.props.BoolProperty(
        name="Script",
        default=False,
        description="Script",
        update=update_ymap_flags) # type: ignore
    
    lod: bpy.props.BoolProperty(
        name="LOD",
        default=False,
        description="LOD",
        update=update_ymap_flags) # type: ignore

class EntityProps(bpy.types.PropertyGroup):
    """Properties for a Entity Definition"""
    enabled: bpy.props.BoolProperty(
        name="Enabled",
        default=True,
        description="Entity toggle",
    ) # type: ignore
    
    linked_object: bpy.props.PointerProperty(
        name="Linked Object",
        type=bpy.types.Object
    )# type: ignore
    
    is_mlo_instance: bpy.props.BoolProperty(
        name="Is MLO Instance",
        default=False) # type: ignore
    
    type: bpy.props.EnumProperty(
        name="Type",
        items=ENTITY_TYPES
    ) # type: ignore
    
    archetype_name: bpy.props.StringProperty(
        name="Archetype Name",
        default="",
        description="Archetype Name") # type: ignore
    
    flags: bpy.props.PointerProperty(
        type=EntityFlags
    ) # type: ignore
    
    guid: bpy.props.StringProperty(
        name="GUID",
        default="",
        description="GUID") # type: ignore
    
    position: bpy.props.FloatVectorProperty(
        name="Position",
        default=(0.0, 0.0, 0.0)) # type: ignore
    
    rotation: bpy.props.FloatVectorProperty(
        name="Rotation",
        size=4,
        default=(0.0, 0.0, 0.0, 0.0)) # type: ignore
    
    scale_xy: bpy.props.FloatProperty(
        name="Scale XY",
        default=0.0) # type: ignore
    
    scale_z: bpy.props.FloatProperty(
        name="Scale Z",
        default=0.0) # type: ignore
    
    parent_index: bpy.props.IntProperty(
        name="Parent Index",
        default=-1) # type: ignore
    
    lod_distance: bpy.props.FloatProperty(
        name="LOD Distance",
        default=0.0) # type: ignore
    
    child_lod_distance: bpy.props.FloatProperty(
        name="Child LOD Distance",
        default=0.0) # type: ignore
    
    num_children: bpy.props.IntProperty(
        name="Num Children",
        default=0) # type: ignore
    
    lod_level: bpy.props.EnumProperty(
        name="LOD Level",
        items=LOD_LEVELS,
        default="LODTYPES_DEPTH_HD",
    ) # type: ignore
    
    priority_level: bpy.props.EnumProperty(
        name="Priority Level",
        items=PRIORITY_LEVELS,
        default="PRI_REQUIRED",
    ) # type: ignore
    
    ambient_occlusion_multiplier: bpy.props.IntProperty(
        name="Ambient Occlusion Multiplier",
        default=255) # type: ignore
    
    artificial_ambient_occlusion: bpy.props.IntProperty(
        name="Artificial Ambient Occlusion",
        default=255) # type: ignore
    
    tint_value: bpy.props.IntProperty(
        name="Tint Value",
        default=0) # type: ignore
    
    group_id: bpy.props.IntProperty(
        name="Group ID",
        default=0) # type: ignore
    
    floor_id: bpy.props.IntProperty(
        name="Floor ID",
        default=0) # type: ignore
    
    mlo_inst_flags: bpy.props.IntProperty(
        name="MLO Instance Flags",
        default=0,
        description="MLO Instance Flags"
    ) # type: ignore
    
    num_exit_portals: bpy.props.IntProperty(
        name="Number of Exit Portals",
        default=0,
        description="Number of exit portals for MLO instances"
    ) # type: ignore
    
    default_entity_sets: bpy.props.CollectionProperty(
        name="Default Entity Sets",
        type=EntitySetsProps) # type: ignore
    
    entity_data_toggle: bpy.props.EnumProperty(
        name="Entity Data Toggle",
        items=ENTITY_TOGGLES # type: ignore
    )

class YmapProps(bpy.types.PropertyGroup):
    is_imported: bpy.props.BoolProperty(
        name="Is Imported",
        default=False,
        description="Is this YMAP imported from a file") # type: ignore
    
    ymap_object: bpy.props.PointerProperty(
        name="Ymap Object",
        type=bpy.types.Object,
        description="Object that contains the YMAP data") # type: ignore
    
    ymap_entity_group_object: bpy.props.PointerProperty(
        name="Ymap Entity Group Object",
        type=bpy.types.Object,
        description="Object that contains the YMAP entity group data") # type: ignore
    
    ymap_occluders_group_object: bpy.props.PointerProperty(
        name="Ymap Occluders Group Object",
        type=bpy.types.Object,
        description="Object that contains the YMAP occluders group data") # type: ignore
    
    ymap_phys_dicts: bpy.props.CollectionProperty(
        name="Ymap Physics Dictionaries",
        type=PhysicsGroup,
        description="Collection of YMAP physics dictionaries") # type: ignore
    
    enabled: bpy.props.BoolProperty(
        name="Enabled",
        default=True,
        description="YMAP toggle") # type: ignore
    
    parent: bpy.props.StringProperty(
        name="Parent",
        default="",
        description="Parent",
        maxlen=60) # type: ignore
    
    flags: bpy.props.PointerProperty(
        type=YmapMapDataFlags
    ) # type: ignore
    
    content_flags: bpy.props.PointerProperty(
        type=YmapMapDataContentFlags
    ) # type: ignore
    
    show_streaming_extents: bpy.props.BoolProperty(
        name="Show Streaming Extents",
        default=False,
        description="Show streaming extents gizmo") # type: ignore
    
    show_entities_extents: bpy.props.BoolProperty(
        name="Show Entities Extents",
        default=False,
        description="Show entities extents gizmo") # type: ignore
    
    streaming_extents_min: bpy.props.FloatVectorProperty(
        name="Streaming Extents Min",
        default=(0.0, 0.0, 0.0),
        description="YMAP streaming extents min") # type: ignore
    
    streaming_extents_max: bpy.props.FloatVectorProperty(
        name="Streaming Extents Max",
        default=(0.0, 0.0, 0.0),
        description="YMAP streaming extents max") # type: ignore
    
    entities_extents_min: bpy.props.FloatVectorProperty(
        name="Entities Extents Min",
        default=(0.0, 0.0, 0.0),
        description="YMAP entities extents min") # type: ignore
    
    entities_extents_max: bpy.props.FloatVectorProperty(
        name="Entities Extents Max",
        default=(0.0, 0.0, 0.0),
        description="YMAP entities extents max") # type: ignore
    
    any_entities: bpy.props.BoolProperty(
        name="Any Entities",
        default=False,
        description="Any entities in the YMAP") # type: ignore
    
    entities: bpy.props.CollectionProperty(
        name="Entities",
        type=EntityProps) # type: ignore
    
    active_category: bpy.props.StringProperty(
        name="Active Category",
        default="",
        description="Active category") # type: ignore
    
    data_category: bpy.props.EnumProperty(
        name="Data Category",
        items=YMAP_MAP_DATA_TOGGLES
    ) # type: ignore

def register():
    bpy.types.Scene.ymap_assets_path = bpy.props.StringProperty(
        name="Asset Path",
        default="",
        description="Sets the path to the asset folder",
        maxlen=60,
        subtype="DIR_PATH")
    
    bpy.types.Scene.ymap_list = bpy.props.CollectionProperty(
        name="Ymaps",
        type=YmapProps)
    
    bpy.types.Scene.ymap_list_index = bpy.props.IntProperty(
        name="Index",
        default=0)
    
    bpy.types.Scene.entity_list_index = bpy.props.IntProperty(
        name="Index",
        default=0,
        update=update_entity_index
    )
    
    bpy.types.Object.vicho_type = bpy.props.StringProperty(
        name="Vicho Type",
        default="vicho_none",
        description="Type of the object, used for filtering in the UI",
        maxlen=60)
    
def unregister():
    del bpy.types.Scene.ymap_assets_path
    del bpy.types.Scene.ymap_list
    del bpy.types.Scene.ymap_list_index
    del bpy.types.Scene.entity_list_index
    del bpy.types.Object.vicho_type