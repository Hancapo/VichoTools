import bpy
from .funcs import ymap_change_index

YMAP_TYPE_TOGGLES = (
    ("MAPDATA", "Map Data", "Map Data", "OUTLINER_DATA_LIGHTPROBE", 0),
    ("ENTITIES", "Entities", "Entities", "OUTLINER_OB_GROUP_INSTANCE", 1),
    ("OCCLUDERS", "Occluders", "Occluders", "GP_CAPS_ROUND", 2),
    ("PHYSICSDICTIONARIES", "Physics Dictionaries", "Physics Dictionaries", "PHYSICS", 3),
    ("INSTANCEDDATA", "Instanced Data", "Instanced Data", "MOD_ARRAY", 4),
    ("TIMECYCLEMODIFIERS", "Timecycle Modifiers", "Timecycle Modifiers", "TIME", 5),
    ("CARGENERATORS", "Car Generators", "Car Generators", "AUTO", 6),
    ("LODLIGHTS", "Lod Lights", "Lod Lights", "LIGHTPROBE_PLANE", 7),
    ("DISTANTLIGHTS", "Distant Lights", "Distant Lights", "LIGHTPROBE_VOLUME", 8),
    ("BLOCK", "Block", "Block", "MESH_PLANE", 9),
)


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
    
    flags: bpy.props.IntProperty(
        name="Flags",
        default=0,
        description="Flags")
    
    content_flags: bpy.props.IntProperty(
        name="Content Flags",
        default=0,
        description="Content Flags")
    
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
        default=0,
        update=ymap_change_index)
    bpy.types.Scene.data_type_toggle = bpy.props.EnumProperty(
        name="Data Type",
        items=YMAP_TYPE_TOGGLES,
        default="MAPDATA")
    
def unregister():
    del bpy.types.Scene.ymap_assets_path
    del bpy.types.Scene.fake_ymap_list
    del bpy.types.Scene.ymap_list_index
    del bpy.types.Scene.data_type_toggle