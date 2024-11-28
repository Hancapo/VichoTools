import bpy
from .helper import (update_content_flags, 
                     update_content_flags_bool_properties, 
                     update_flags_bool_properties, 
                     update_flags, 
                     YMAP_MAP_DATA_TOGGLES, 
                     YMAP_TYPE_TOGGLES)


class YmapMapDataContentFlags(bpy.types.PropertyGroup):
    total_flags: bpy.props.IntProperty(
        name="Flags",
        default=0,
        min=0,
        description="YMAP flags",
        update=update_content_flags_bool_properties)
    hd: bpy.props.BoolProperty(
        name="HD",
        default=False,
        description="HD",
        update=update_content_flags)
    
    lod: bpy.props.BoolProperty(
        name="LOD",
        default=False,
        description="LOD",
        update=update_content_flags)
    
    slod2_plus: bpy.props.BoolProperty(
        name="SLOD2+",
        default=False,
        description="SLOD2+",
        update=update_content_flags)
    
    interior: bpy.props.BoolProperty(
        name="Interior",
        default=False,
        description="Interior",
        update=update_content_flags)
    
    slod: bpy.props.BoolProperty(
        name="SLOD",
        default=False,
        description="SLOD",
        update=update_content_flags)
    
    occlusion: bpy.props.BoolProperty(
        name="Occlusion",
        default=False,
        description="Occlusion",
        update=update_content_flags)
    
    physics: bpy.props.BoolProperty(
        name="Physics",
        default=False,
        description="Physics",
        update=update_content_flags)
    
    lod_lights: bpy.props.BoolProperty(
        name="LOD Lights",
        default=False,
        description="LOD Lights",
        update=update_content_flags)
    
    distant_lights: bpy.props.BoolProperty(
        name="Distant Lights",
        default=False,
        description="Distant Lights",
        update=update_content_flags)
    
    critical: bpy.props.BoolProperty(
        name="Critical",
        default=False,
        description="Critical",
        update=update_content_flags)
    
    grass: bpy.props.BoolProperty(
        name="Grass",
        default=False,
        description="Grass",
        update=update_content_flags)

class YmapMapDataFlags(bpy.types.PropertyGroup):
    total_flags: bpy.props.IntProperty(
        name="Flags",
        default=0,
        min=0,
        description="YMAP content flags",
        update=update_flags_bool_properties)
    
    script: bpy.props.BoolProperty(
        name="Script",
        default=False,
        description="Script",
        update=update_flags)
    
    lod: bpy.props.BoolProperty(
        name="LOD",
        default=False,
        description="LOD",
        update=update_flags)

class EntityProps(bpy.types.PropertyGroup):
    archetype_name: bpy.props.StringProperty(
        name="Archetype Name",
        default="",
        description="Archetype Name")
    flags: bpy.props.IntProperty(
        name="Flags",
        default=0)
    
    guid: bpy.props.StringProperty(
        name="GUID",
        default="",
        description="GUID")
    
    position: bpy.props.FloatVectorProperty(
        name="Position",
        default=(0.0, 0.0, 0.0))
    
    rotation: bpy.props.FloatVectorProperty(
        name="Rotation",
        default=(0.0, 0.0, 0.0))
    
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
    
    lod_level: bpy.props.StringProperty(
        name="LOD Level",
        default="")
    
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
    
    tintValue: bpy.props.IntProperty(
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