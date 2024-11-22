import bpy

class BlockProps(bpy.types.PropertyGroup):
    version: bpy.props.IntProperty(
        name="Version",
        default=0,
        description="Block Version")
    flags: bpy.props.IntProperty(
        name="Flags",
        default=0,
        description="Block Flags")
    name: bpy.props.StringProperty(
        name="Name",
        default="",
        description="Block Name",
        maxlen=60)
    exported_by: bpy.props.StringProperty(
        name="Exported By",
        default="",
        description="Block Exported By",
        maxlen=60)
    owner: bpy.props.StringProperty(
        name="Owner",
        default="",
        description="Block Owner",
        maxlen=60)
    time: bpy.props.StringProperty(
        name="Time",
        default="",
        description="Block Time",
        maxlen=60)

class EntityDefProps(bpy.types.PropertyGroup):
    pass

class MapDataProps(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Name",
        default="",
        description="YMAP Name",
        maxlen=60)
    parent: bpy.props.StringProperty(
        name="Parent",
        default="",
        description="YMAP Parent",
        maxlen=60)
    flags: bpy.props.IntProperty(
        name="Flags",
        default=0,
        description="YMAP Flags")
    content_flags: bpy.props.IntProperty(
        name="Content Flags",
        default=0,
        description="YMAP Content Flags")
    streaming_extents_min: bpy.props.FloatVectorProperty(
        name="Streaming Extents Min",
        default=(0.0, 0.0, 0.0),
        description="YMAP Streaming Extents Min")
    streaming_extents_max: bpy.props.FloatVectorProperty(
        name="Streaming Extents Max",
        default=(0.0, 0.0, 0.0),
        description="YMAP Streaming Extents Max")
    entities_extents_min: bpy.props.FloatVectorProperty(
        name="Entities Extents Min",
        default=(0.0, 0.0, 0.0),
        description="YMAP Entities Extents Min")
    entities_extents_max: bpy.props.FloatVectorProperty(
        name="Entities Extents Max",
        default=(0.0, 0.0, 0.0),
        description="YMAP Entities Extents Max")
    
class YmapProps(bpy.types.PropertyGroup):
    map_data: bpy.props.PointerProperty(
        name="Map Data",
        type=MapDataProps)
    block: bpy.props.PointerProperty(
        name="Block",
        type=BlockProps)
    entities: bpy.props.CollectionProperty(
        name="Entities",
        type=EntityDefProps)
    enabled: bpy.props.BoolProperty(
        name="Enabled",
        default=True,
        description="Enabled")
    

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
    
def unregister():
    del bpy.types.Scene.ymap_assets_path
    del bpy.types.Scene.ymap_list
    del bpy.types.Scene.ymap_list_index