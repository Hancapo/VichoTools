from mathutils import Vector
import bpy
import string
import time
import uuid
import random
from bpy.types import Object, Collection, Mesh

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

def is_object_in_scene(obj):
    return obj.name in bpy.context.scene.collection.objects

def is_drawable_model(obj):
    return obj.sollum_type == 'sollumz_drawable_model'

def is_mesh(obj):
    return obj.type == 'MESH'

def is_drawable(obj):
    return obj.sollum_type == 'sollumz_drawable'

def gen_rdm_str(length=8):
    chars = string.ascii_letters + string.digits
    rd_part = ''.join(random.choice(chars) for _ in range(length))
    ts = str(int(time.time()))[-4:]
    uuid_str = str(uuid.uuid4()).replace('-', '')[:4]
    rdm_str = f"{rd_part}{ts}{uuid_str}"
    return rdm_str

def abs_path(path: str) -> str:
    return bpy.path.abspath(path)

def is_obj_in_any_collection(obj):
    return any(obj.name in collection.objects for collection in bpy.data.collections)

def get_top_parent(obj):
    while obj.parent:
        obj = obj.parent
    return obj

def add_transform_item(self, context):
    obj: Object = context.active_object
    if obj:
        new_transform = obj.transforms_list.add()
        new_transform.name = f"Transform {len(obj.transforms_list)}"
        new_transform.location = obj.location.copy()
        obj.rotation_mode = 'XYZ'
        new_transform.rotation = obj.rotation_euler.copy()
        new_transform.scale = obj.scale.copy()
        obj.active_transform_index = len(obj.transforms_list) - 1
        return new_transform
    
def remove_transform_item_by_index(self, context, index):
    obj: Object = context.active_object
    if obj and obj.transforms_list:
        if 0 <= index < len(obj.transforms_list):
            obj.transforms_list.remove(index)
            if len(obj.transforms_list) > 0:
                obj.active_transform_index = min(obj.active_transform_index, len(obj.transforms_list) - 1)
            else:
                obj.active_transform_index = -1
    return None

def set_obj_to_transform_item(self, context, index):
    obj: Object = context.active_object
    if obj and obj.transforms_list:
        if 0 <= index < len(obj.transforms_list):
            transform_item = obj.transforms_list[index]
            obj.location = transform_item.location
            obj.rotation_euler = transform_item.rotation
            obj.scale = transform_item.scale
            return True
    return False

def reset_transform_obj(self, context):
    obj: Object = context.active_object
    obj.location = (0, 0, 0)
    obj.rotation_euler = (0, 0, 0)
    obj.scale = (1, 1, 1)

def update_transform_index(self, context):
    if context.scene.lock_transform:
        return
    set_obj_to_transform_item(self, context, self.active_transform_index)
    obj = context.active_object
    obj.select_set(True)
    
    if context.scene.zoom_to_object:
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        with context.temp_override(area=area, region=region):
                            bpy.ops.view3d.view_selected()
                        return
                    
def create_empty_obj(name: str, collection: Collection = None):
    """Create an empty object with the given name."""
    empty_obj = bpy.data.objects.new(name, None)
    empty_obj.empty_display_type = "PLAIN_AXES"
    empty_obj.empty_display_size = 0.0001
    empty_obj.name = name
    if collection:
        collection.objects.link(empty_obj)
    else:
        bpy.context.scene.collection.objects.link(empty_obj)
    return empty_obj

def create_ymap_empty(name: str, collection: Collection = None):
    """Create an empty object for a YMAP."""
    ymap_obj = create_empty_obj(name, collection)
    ymap_obj.vicho_type = 'vicho_ymap_base'
    return ymap_obj

def create_ymap_entities_group(parent_ymap_obj: Object):
    """Create a group for YMAP entities."""
    ymap_entities_group = create_empty_obj(f"{parent_ymap_obj.name}.entities")
    ymap_entities_group.vicho_type = 'vicho_ymap_entities'
    ymap_entities_group.parent = parent_ymap_obj
    return ymap_entities_group

def obj_has_parent(obj: Object) -> bool:
    """Check if the object has a parent."""
    return obj.parent is not None

def delete_obj(obj):
    """Delete the given object and its data if unused."""
    bpy.data.objects.remove(obj, do_unlink=True)

def delete_unused_objs_from_scene(self):
    """Delete all objects not in the scene."""
    for obj in bpy.context.scene.objects:
        if not is_object_in_scene(obj):
            delete_obj(obj)

def get_hierarchy(root: Object) -> list[Object]:
    """Collect root and all its descendants."""
    objs = []
    def recurse(obj):
        objs.append(obj)
        for child in obj.children:
            recurse(child)
    recurse(root)
    return objs

def delete_hierarchy(root: Object):
    """Delete the root object and all its descendants."""
    to_delete = get_hierarchy(root)
    for obj in to_delete:
        for col in list(obj.users_collection):
            col.objects.unlink(obj)
    for obj in reversed(to_delete):
        data = getattr(obj, "data", None)
        if data and data.users == 0:
            if isinstance(data, bpy.types.Mesh):
                bpy.data.meshes.remove(data)
        delete_obj(obj)
        
def delete_mesh(mesh: Mesh):
    """Delete the given mesh even if it has users."""
    if mesh.users == 0:
        bpy.data.meshes.remove(mesh)
    else:
        for obj in bpy.data.objects:
            if obj.data == mesh:
                obj.data = None
        bpy.data.meshes.remove(mesh, do_unlink=True)
        
def try_parse_int(value: str) -> int | None:
    """Try to parse a string as an integer."""
    try:
        return int(value)
    except ValueError:
        return None