from mathutils import Vector
import bpy
from .ytd_helper import YtdItem


def get_bounds_from_single_object(obj):
    corners = []

    for pos in obj.bound_box:
        corners.append(Vector(pos))

    return corners


def get_bound_extents(obj, margin=0):
    corners = get_bounds_from_single_object(obj)

    if not corners:
        return Vector(), Vector()

    min = subtract_from_vector(get_min_vector_list(corners), margin)
    max = add_to_vector(get_max_vector_list(corners), margin)
    return min + obj.location, max + obj.location


def subtract_from_vector(v, f):
    r = Vector((0, 0, 0))
    r.x = v.x - f
    r.y = v.y - f
    r.z = v.z - f
    return r


def add_to_vector(v, f):
    r = Vector((0, 0, 0))
    r.x = v.x + f
    r.y = v.y + f
    r.z = v.z + f
    return r


def get_min_vector_list(vecs):
    x = []
    y = []
    z = []
    for v in vecs:
        x.append(v[0])
        y.append(v[1])
        z.append(v[2])
    return Vector((min(x), min(y), min(z)))


def get_max_vector_list(vecs):
    x = []
    y = []
    z = []
    for v in vecs:
        x.append(v[0])
        y.append(v[1])
        z.append(v[2])
    return Vector((max(x), max(y), max(z)))


class VichoGroup(bpy.types.PropertyGroup):
    bpy.types.Scene.file_name_field = bpy.props.StringProperty(
        name="File Name",
        default="",
        description="File name for the text file",
        maxlen=50)

    bpy.types.Scene.ymap_instance_name_field = bpy.props.StringProperty(
        name="Instance Name",
        default="",
        description="instance name for the MLO Instance",
        maxlen=50)
    bpy.types.Scene.location_checkbox = bpy.props.BoolProperty(
        name="Reset Location",
        description="Reset location")
    bpy.types.Scene.rotation_checkbox = bpy.props.BoolProperty(
        name="Reset Rotation",
        description="Reset rotation")
    bpy.types.Scene.scale_checkbox = bpy.props.BoolProperty(
        name="Reset Scale",
        description="Reset scale")
    bpy.types.Scene.CopyDataFromObject = bpy.props.PointerProperty(
        name="Copy Data From Object",
        type=bpy.types.Object)
    bpy.types.Scene.PasteDataToObject = bpy.props.PointerProperty(
        name="Paste Data To Object",
        type=bpy.types.Object)

    bpy.types.Scene.locationOb_checkbox = bpy.props.BoolProperty(
        name="Location",
        description="Location")
    bpy.types.Scene.rotationOb_checkbox = bpy.props.BoolProperty(
        name="Rotation",
        description="Rotation")
    bpy.types.Scene.scaleOb_checkbox = bpy.props.BoolProperty(
        name="Scale",
        description="Scale")

    bpy.types.Scene.ytd_export_path = bpy.props.StringProperty(
        name="YTD Export Path",
        default="",
        description="Path to export the YTD file",
        subtype='DIR_PATH'
    )
