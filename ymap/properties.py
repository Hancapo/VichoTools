import bpy
from .constants import (
                     YMAP_MAP_DATA_TOGGLES, 
                     YMAP_TYPE_TOGGLES,
                     ENTITY_TOGGLES,
                     LOD_LEVELS,
                     ENTITY_TYPES)

from .helper import (update_entity_flags_bool_properties, 
                     update_entity_flags, 
                     update_ymap_flags_bool_properties, 
                     update_ymap_flags, 
                     update_ymap_content_flags_bool_properties, 
                     update_ymap_content_flags)

class EntityFlags(bpy.types.PropertyGroup):
    total_flags: bpy.props.IntProperty(
        name="Flags",
        default=0,
        min=0,
        description="Entity flags",
        update=update_entity_flags_bool_properties)
    allow_full_rotation: bpy.props.BoolProperty(
        name="Allow Full Rotation",
        default=False,
        description="Allow Full Rotation",
        update=update_entity_flags)
    
    stream_low_priority: bpy.props.BoolProperty(
        name="Stream Low Priority",
        default=False,
        description="Stream Low Priority",
        update=update_entity_flags)
    
    disable_embedded_collision: bpy.props.BoolProperty(
        name="Disable Embedded Collision",
        default=False,
        description="Disable Embedded Collision",
        update=update_entity_flags)
    
    lod_in_parent_map: bpy.props.BoolProperty(
        name="LOD In Parent Map",
        default=False,
        description="LOD In Parent Map",
        update=update_entity_flags)
    
    lod_adopt_me: bpy.props.BoolProperty(
        name="LOD Adopt Me",
        default=False,
        description="LOD Adopt Me",
        update=update_entity_flags)
    
    static_entity: bpy.props.BoolProperty(
        name="Static Entity",
        default=False,
        description="Static Entity",
        update=update_entity_flags)
    
    interior_lod: bpy.props.BoolProperty(
        name="Interior LOD",
        default=False,
        description="Interior LOD",
        update=update_entity_flags)
    
    lod_use_alt_fade: bpy.props.BoolProperty(
        name="LOD Use Alt Fade",
        default=False,
        description="LOD Use Alt Fade",
        update=update_entity_flags)
    
    underwater: bpy.props.BoolProperty(
        name="Underwater",
        default=False,
        description="Underwater",
        update=update_entity_flags)
    
    doesnt_touch_water: bpy.props.BoolProperty(
        name="Doesn't Touch Water",
        default=False,
        description="Doesn't Touch Water",
        update=update_entity_flags)
    
    doesnt_spawn_peds: bpy.props.BoolProperty(
        name="Doesn't Spawn Peds",
        default=False,
        description="Doesn't Spawn Peds",
        update=update_entity_flags)
    
    cast_static_shadows: bpy.props.BoolProperty(
        name="Cast Static Shadows",
        default=False,
        description="Cast Static Shadows",
        update=update_entity_flags)
    
    cast_dynamic_shadows: bpy.props.BoolProperty(
        name="Cast Dynamic Shadows",
        default=False,
        description="Cast Dynamic Shadows",
        update=update_entity_flags)
    
    ignore_time_settings: bpy.props.BoolProperty(
        name="Ignore Time Settings",
        default=False,
        description="Ignore Time Settings",
        update=update_entity_flags)
    
    dont_render_shadows: bpy.props.BoolProperty(
        name="Don't Render Shadows",
        default=False,
        description="Don't Render Shadows",
        update=update_entity_flags)
    
    only_render_shadows: bpy.props.BoolProperty(
        name="Only Render Shadows",
        default=False,
        description="Only Render Shadows",
        update=update_entity_flags)
    
    dont_render_reflections: bpy.props.BoolProperty(
        name="Don't Render Reflections",
        default=False,
        description="Don't Render Reflections",
        update=update_entity_flags)
    
    only_render_reflections: bpy.props.BoolProperty(
        name="Only Render Reflections",
        default=False,
        description="Only Render Reflections",
        update=update_entity_flags)
    
    dont_render_water_reflections: bpy.props.BoolProperty(
        name="Don't Render Water Reflections",
        default=False,
        description="Don't Render Water Reflections",
        update=update_entity_flags)
    
    only_render_water_reflections: bpy.props.BoolProperty(
        name="Only Render Water Reflections",
        default=False,
        description="Only Render Water Reflections",
        update=update_entity_flags)
    
    dont_render_mirror_reflections: bpy.props.BoolProperty(
        name="Don't Render Mirror Reflections",
        default=False,
        description="Don't Render Mirror Reflections",
        update=update_entity_flags)
    
    only_render_mirror_reflections: bpy.props.BoolProperty(
        name="Only Render Mirror Reflections",
        default=False,
        description="Only Render Mirror Reflections",
        update=update_entity_flags)

class YmapMapDataContentFlags(bpy.types.PropertyGroup):
    total_flags: bpy.props.IntProperty(
        name="Flags",
        default=0,
        min=0,
        description="YMAP flags",
        update=update_ymap_content_flags_bool_properties)
    hd: bpy.props.BoolProperty(
        name="HD",
        default=False,
        description="HD",
        update=update_ymap_content_flags)
    
    lod: bpy.props.BoolProperty(
        name="LOD",
        default=False,
        description="LOD",
        update=update_ymap_content_flags)
    
    slod2_plus: bpy.props.BoolProperty(
        name="SLOD2+",
        default=False,
        description="SLOD2+",
        update=update_ymap_content_flags)
    
    interior: bpy.props.BoolProperty(
        name="Interior",
        default=False,
        description="Interior",
        update=update_ymap_content_flags)
    
    slod: bpy.props.BoolProperty(
        name="SLOD",
        default=False,
        description="SLOD",
        update=update_ymap_content_flags)
    
    occlusion: bpy.props.BoolProperty(
        name="Occlusion",
        default=False,
        description="Occlusion",
        update=update_ymap_content_flags)
    
    physics: bpy.props.BoolProperty(
        name="Physics",
        default=False,
        description="Physics",
        update=update_ymap_content_flags)
    
    lod_lights: bpy.props.BoolProperty(
        name="LOD Lights",
        default=False,
        description="LOD Lights",
        update=update_ymap_content_flags)
    
    distant_lights: bpy.props.BoolProperty(
        name="Distant Lights",
        default=False,
        description="Distant Lights",
        update=update_ymap_content_flags)
    
    critical: bpy.props.BoolProperty(
        name="Critical",
        default=False,
        description="Critical",
        update=update_ymap_content_flags)
    
    grass: bpy.props.BoolProperty(
        name="Grass",
        default=False,
        description="Grass",
        update=update_ymap_content_flags)

class YmapMapDataFlags(bpy.types.PropertyGroup):
    total_flags: bpy.props.IntProperty(
        name="Flags",
        default=0,
        min=0,
        description="YMAP content flags",
        update=update_ymap_flags_bool_properties)
    
    script: bpy.props.BoolProperty(
        name="Script",
        default=False,
        description="Script",
        update=update_ymap_flags)
    
    lod: bpy.props.BoolProperty(
        name="LOD",
        default=False,
        description="LOD",
        update=update_ymap_flags)

class EntityProps(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(
        name="Enabled",
        default=True,
    )
    entity_data_toggle: bpy.props.EnumProperty(
        name="Data Type",
        items=ENTITY_TOGGLES)
    
    linked_object: bpy.props.PointerProperty(
        name="Linked Object",
        type=bpy.types.Object
    )
    
    is_mlo_instance: bpy.props.BoolProperty(
        name="Is MLO Instance",
        default=False)
    
    type: bpy.props.EnumProperty(
        name="Type",
        items=ENTITY_TYPES
    )
    
    archetype_name: bpy.props.StringProperty(
        name="Archetype Name",
        default="",
        description="Archetype Name")
    
    flags: bpy.props.PointerProperty(
        type=EntityFlags
    )
    
    guid: bpy.props.StringProperty(
        name="GUID",
        default="",
        description="GUID")
    
    position: bpy.props.FloatVectorProperty(
        name="Position",
        default=(0.0, 0.0, 0.0))
    
    rotation: bpy.props.FloatVectorProperty(
        name="Rotation",
        size=4,
        default=(0.0, 0.0, 0.0, 0.0))
    
    scale_xy: bpy.props.FloatProperty(
        name="Scale XY",
        default=0.0)
    
    scale_z: bpy.props.FloatProperty(
        name="Scale Z",
        default=0.0)
    
    parent_index: bpy.props.IntProperty(
        name="Parent Index",
        default=-1)
    
    lod_distance: bpy.props.FloatProperty(
        name="LOD Distance",
        default=0.0)
    
    child_lod_distance: bpy.props.FloatProperty(
        name="Child LOD Distance",
        default=0.0)
    
    num_children: bpy.props.IntProperty(
        name="Num Children",
        default=0)
    
    lod_level: bpy.props.EnumProperty(
        name="LOD Level",
        items=LOD_LEVELS
    )
    
    priority_level: bpy.props.StringProperty(
        name="Priority Level",
        default=""
    )
    
    ambient_occlusion_multiplier: bpy.props.IntProperty(
        name="Ambient Occlusion Multiplier",
        default=0)
    
    artificial_ambient_occlusion: bpy.props.IntProperty(
        name="Artificial Ambient Occlusion",
        default=0)
    
    tint_value: bpy.props.IntProperty(
        name="Tint Value",
        default=0)

class YmapProps(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(
        name="Enabled",
        default=True,
        description="YMAP toggle")
    
    name: bpy.props.StringProperty(
        name="Name",
        default="",
        description="Name",
        maxlen=60)
    
    parent: bpy.props.StringProperty(
        name="Parent",
        default="",
        description="Parent",
        maxlen=60)
    
    flags: bpy.props.PointerProperty(
        type=YmapMapDataFlags
    )
    
    content_flags: bpy.props.PointerProperty(
        type=YmapMapDataContentFlags
    )
    
    streaming_extents_min: bpy.props.FloatVectorProperty(
        name="Streaming Extents Min",
        default=(0.0, 0.0, 0.0),
        description="YMAP streaming extents min")
    
    streaming_extents_max: bpy.props.FloatVectorProperty(
        name="Streaming Extents Max",
        default=(0.0, 0.0, 0.0),
        description="YMAP streaming extents max")
    
    entities_extents_min: bpy.props.FloatVectorProperty(
        name="Entities Extents Min",
        default=(0.0, 0.0, 0.0),
        description="YMAP entities extents min")
    
    entities_extents_max: bpy.props.FloatVectorProperty(
        name="Entities Extents Max",
        default=(0.0, 0.0, 0.0),
        description="YMAP entities extents max")
    
    map_data_toggle: bpy.props.EnumProperty(
        name="Map Data",
        items=YMAP_MAP_DATA_TOGGLES)
    
    hash: bpy.props.StringProperty(
        name="Hash",
        default="",
        description="Hash")
    
    any_entities: bpy.props.BoolProperty(
        name="Any Entities",
        default=False,
        description="Any entities in the YMAP")
    
    entities: bpy.props.CollectionProperty(
        name="Entities",
        type=EntityProps)

def register():
    bpy.types.Scene.ymap_assets_path = bpy.props.StringProperty(
        name="Asset Path",
        default="",
        description="Sets the path to the asset folder",
        maxlen=60,
        subtype="DIR_PATH")
    
    bpy.types.Scene.fake_ymap_list = bpy.props.CollectionProperty(
        name="Ymaps",
        type=YmapProps)
    bpy.types.Scene.ymap_list_index = bpy.props.IntProperty(
        name="Index",
        default=0)
    bpy.types.Scene.entity_list_index = bpy.props.IntProperty(
        name="Index",
        default=0)
    bpy.types.Scene.data_type_toggle = bpy.props.EnumProperty(
        name="Data Type",
        items=YMAP_TYPE_TOGGLES)
    
def unregister():
    del bpy.types.Scene.ymap_assets_path
    del bpy.types.Scene.fake_ymap_list
    del bpy.types.Scene.ymap_list_index
    del bpy.types.Scene.data_type_toggle