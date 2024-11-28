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
    bpy.types.Scene.data_type_toggle = bpy.props.EnumProperty(
        name="Data Type",
        items=YMAP_TYPE_TOGGLES)
    
def unregister():
    del bpy.types.Scene.ymap_assets_path
    del bpy.types.Scene.fake_ymap_list
    del bpy.types.Scene.ymap_list_index
    del bpy.types.Scene.data_type_toggle