import bpy

class AnimProps(bpy.types.PropertyGroup):
    bpy.types.Scene.ycd_name = bpy.props.StringProperty(
        name="YCD Name",
        default="",
        description="YCD Name",
        maxlen=60)