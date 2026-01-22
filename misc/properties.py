import bpy
from .helper import update_transform_index

class TransformItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="NewTransform")  # type: ignore
    location: bpy.props.FloatVectorProperty(name="Location", subtype='TRANSLATION', size=3, default=(0.0, 0.0, 0.0)) # type: ignore
    rotation: bpy.props.FloatVectorProperty(name="Rotation", subtype='EULER', size=3, default=(0.0, 0.0, 0.0)) # type: ignore
    scale: bpy.props.FloatVectorProperty(name="Scale", subtype='XYZ', size=3, default=(1.0, 1.0, 1.0)) # type: ignore


def register():
    bpy.types.Object.transforms_list = bpy.props.CollectionProperty(type=TransformItem)
    bpy.types.Object.active_transform_index = bpy.props.IntProperty(name="Active Transform Index", default=0, update=update_transform_index)
    bpy.types.Scene.lock_transform = bpy.props.BoolProperty(name="Lock Transform", default=False)
    bpy.types.Scene.zoom_to_object = bpy.props.BoolProperty(name="Zoom to Object", default=False)