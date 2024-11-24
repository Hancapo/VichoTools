import bpy

class YmapProps(bpy.types.PropertyGroup):
    enabled: bpy.props.BoolProperty(
        name="Enabled",
        default=True,
        description="YMAP toggle")
    

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