import bpy
from bpy.types import Object, Collection, Mesh
from mathutils import Vector
from .funcs import (
    subtract_from_vector,
    add_to_vector,
    get_min_vector_list,
    get_max_vector_list,
    try_parse_int,
    mask_to_enum,
    enum_to_mask,
    enum_items_to_valid_mask,
)
from ..vicho_dependencies import dependencies_manager as d
from .constants import YMAP_ENTITY_SOLLUM_TYPES, COMPAT_OBJECT_TYPES
from bpy.ops import _BPyOpsSubModOp


class IndexHelper:
    index: bpy.props.IntProperty() # type: ignore

def is_object_in_scene(obj: Object) -> bool:
    """Check if the object is in the current scene's collection."""
    return obj.name in bpy.context.scene.collection.objects


def is_drawable_model(obj: Object) -> bool:
    """Check if the object is a Drawable Model (Sollumz)."""
    return obj.sollum_type == "sollumz_drawable_model"


def is_mesh(obj: Object) -> bool:
    """Whether the object is a mesh."""
    return obj.type == "MESH"


def is_drawable(obj: Object) -> bool:
    """Check if the object is a Drawable (Sollumz)."""
    return obj.sollum_type == "sollumz_drawable"


def get_bounds_from_single_object(obj: Object) -> list[Vector]:
    """Return the object's bounding box corners in local space."""
    corners = []
    for pos in obj.bound_box:
        corners.append(Vector(pos))
    return corners


def get_bound_extents(obj, margin=0):
    """
    Return the object's bounding box min/max vectors,
    with location applied.
    """
    corners = get_bounds_from_single_object(obj)

    if not corners:
        return Vector(), Vector()

    vmin = subtract_from_vector(get_min_vector_list(corners), margin)
    vmax = add_to_vector(get_max_vector_list(corners), margin)
    return vmin + obj.location, vmax + obj.location


def abs_path(path: str) -> str:
    """Get the absolute path from a relative path using Blender's path system."""
    return bpy.path.abspath(path)


def is_obj_in_any_collection(obj: Object) -> bool:
    """Check if the object is in any collection."""
    return any(obj.name in collection.objects for collection in bpy.data.collections)


def create_obj(name: str, link_to_scene: bool = False, mesh: Mesh = None) -> Object:
    """Create a new object with the given name and optional mesh data."""
    new_obj = bpy.data.objects.new(name, mesh)
    if link_to_scene:
        link_obj_to_main_collection(new_obj)
    return new_obj

def create_mesh_from_data(name: str, verts: list[Vector], faces: list[tuple], edges: list[tuple] = None) -> Mesh:
    """Create a new mesh from given vertex, edge, and face data."""
    if edges is None:
        edges = []
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, edges, faces)
    mesh.update()
    return mesh

def get_top_parent(obj: Object) -> Object:
    """Get the top-most parent of the given object."""
    while obj.parent:
        obj = obj.parent
    return obj


def reset_obj_transform(obj: Object) -> None:
    """Reset the object's transform to default values."""
    obj.location = (0, 0, 0)
    obj.rotation_euler = (0, 0, 0)
    obj.scale = (1, 1, 1)


def create_empty_obj(name: str, collection: Collection = None) -> Object | None:
    """Create an empty object with the given name."""
    empty_obj = bpy.data.objects.new(name, None)
    empty_obj.empty_display_type = "PLAIN_AXES"
    empty_obj.empty_display_size = 0.0001
    empty_obj.name = name
    if collection:
        collection.objects.link(empty_obj)
    else:
        link_obj_to_main_collection(empty_obj)
    return empty_obj


def link_obj_to_main_collection(obj: Object) -> None:
    """Link the object to the main scene collection."""
    if obj.name not in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.link(obj)


def obj_has_parent(obj: Object) -> bool:
    """Check if the object has a parent."""
    return obj.parent is not None


def delete_obj(obj: Object) -> None:
    """Delete the given object and its data if unused."""
    bpy.data.objects.remove(obj, do_unlink=True)


def delete_unused_objs_from_scene() -> None:
    """Delete all objects not in the scene."""
    for obj in bpy.context.scene.objects:
        if not is_object_in_scene(obj):
            delete_obj(obj)


def get_meta_hash(name: str):
    """Get the meta hash for a given name."""
    int_hash: int | None = try_parse_int(name)
    return (
        d.MetaHash(d.JenkHash.GenHash(name))
        if int_hash is None
        else d.MetaHash(int_hash)
    )

def get_hierarchy(root: Object) -> list[Object]:
    """Collect root and all its descendants."""
    return [root, *root.children_recursive]

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
        
def delete_mesh(mesh: Mesh) -> None:
    """Delete a mesh and unlink it from all objects."""
    if mesh.users == 0:
        bpy.data.meshes.remove(mesh)
    else:
        for obj in bpy.data.objects:
            if obj.data == mesh:
                obj.data = None
        bpy.data.meshes.remove(mesh, do_unlink=True)

def get_path_from_folder_dialog() -> str | None:
    """Open a folder dialog and return the selected path."""
    file_browser = d.FolderBrowser()
    result = file_browser.GetSelectedPath()
    return result if result else None

def is_active_obj() -> bool:
    """Check if there is an active object in the context."""
    return bpy.context.active_object is not None

def get_active_obj() -> Object | None:
    """Get the active object in the context."""
    return bpy.context.active_object

def has_active_obj_parent() -> bool:
    """Check if the active object has a parent."""
    active_obj = get_active_obj()
    return active_obj is not None and active_obj.parent is not None


def zoom_to_objs() -> None:
    """Zoom the 3D view to fit the given object(s)."""
    context = bpy.context
    for area in context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    with context.temp_override(area=area, region=region):
                        bpy.ops.view3d.view_selected()
                    return

def world_corners_of(obj):
    """Return the 8 world-space corners of the object's bounding box."""
    bb = obj.bound_box
    if not bb:
        return ()
    return (obj.matrix_world @ Vector(c) for c in bb)

def force_area_redraw(context) -> None:
    """Forces a redraw of all areas in the context"""
    for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()

def get_mask(self, prop_name):
    """Get the mask value of the enum property."""
    prop = getattr(self, prop_name, None)
    return 0 if prop is None else enum_to_mask(prop)

def set_mask(self, prop_name, value, enum_items):
    """Set the enum property based on the given mask value."""
    valid_mask = enum_items_to_valid_mask(enum_items)
    m = int(value) & valid_mask
    setattr(self, prop_name, mask_to_enum(m, enum_items))

def resolve_hashes_from_file(file_path: str) -> None:
    """Load hashes from a text file into CodeWalker's JenkIndex."""
    all_txt_lines: list[str] = open(file_path, "r").readlines()
    for line in all_txt_lines:
        d.JenkIndex.Ensure(line.strip())

def str_loaded_count() -> int:
    """Return the count of loaded strings within CodeWalker's String indexes."""
    if d.available:
        return d.JenkIndex.GetAllStrings().Length
    else:
        return None
    
def run_ops_without_view_layer_update(func) -> None:
    """Run a function without triggering view layer updates."""
    view_layer_update = _BPyOpsSubModOp._view_layer_update
    def dummy_view_layer_update(context):
        pass
    try:
        _BPyOpsSubModOp._view_layer_update = dummy_view_layer_update
        func()
    finally:
        _BPyOpsSubModOp._view_layer_update = view_layer_update

def instance_obj(obj: Object) -> Object:
    """Instance the given object."""
    new_obj: Object = obj.copy()
    if obj.data:
        new_obj.data = obj.data
    for collection in obj.users_collection:
        collection.objects.link(new_obj)
    return new_obj

def instance_obj_and_child(obj: Object) -> Object:
    """Instance an object and its children recursively, returning the new root."""
    new_root = instance_obj(obj)
    for child in obj.children:
        instance_obj_and_child_recur(child, new_root)
    return new_root

def instance_obj_and_child_recur(obj: Object, parent: Object):
    """Helper function to instance an object and its children recursively."""
    new_obj: Object = instance_obj(obj)
    new_obj.parent = parent
    for child in obj.children:
        instance_obj_and_child_recur(child, new_obj)

def get_obj_from_scene(scene, obj_name: Object) -> Object:
    """Get an object by name from the given scene."""
    return scene.objects.get(obj_name)

def get_scene_collection(scene) -> str:
    """Returns the name of the scene collection"""
    return scene.collection.name if scene.collection else "Scene Collection"

def get_sollumz_settings() -> bpy.types.AddonPreferences:
    """Returns the Sollumz addon preferences"""
    loaded_addons = bpy.context.preferences.addons
    for addon in loaded_addons:
        if "sollumz" in addon.module:
            return loaded_addons[addon.module].preferences
    return None

def set_sollumz_export_format_to_binary() -> bpy.types.AddonPreferences:
    """Returns the Sollumz target formats for export"""
    preferences = get_sollumz_settings()
    if preferences:
        preferences.export_settings.target_formats = {'NATIVE'}

def set_sollumz_gen_ver(gen_version: str) -> None:
    """Sets the GTA V version for export. 
    
    Versions
    --------------- 
    * 8 -> Legacy
    * 9 -> Enhanced"""

    versions: tuple = tuple()
    if "Legacy" in gen_version:
        versions += ('GEN8',)
    if "Enhanced" in gen_version:
        versions += ('GEN9',)

    preferences = get_sollumz_settings()
    if preferences:
        preferences.export_settings.target_versions = set(versions)

def set_sollumz_export_settings() -> None:
    """Sets the proper settings needed for assets export"""
    preferences = get_sollumz_settings()
    if preferences:
        preferences.export_settings.limit_to_selected = True
        preferences.export_settings.apply_transforms = False
        
def set_sollumz_import_settings() -> None:
    """Sets the proper settings needed for assets import"""
    preferences = get_sollumz_settings()
    if preferences:
        preferences.import_settings.import_as_asset = False
        preferences.import_settings.split_by_group = False
        preferences.import_settings.import_ext_skeleton = False

def set_sollumz_export_path(export_path: str) -> None:
    """Sets the export path for Sollumz"""
    scene = bpy.context.scene
    scene.sollumz_export_path = export_path

def clear_sollumz_export_path() -> None:
    """Clears the export path for Sollumz"""
    set_sollumz_export_path("")

def get_sel_objs_list(context) -> list[Object]:
    """Returns a list of selected objects in the context"""
    objs: list[Object] = []
    for obj in context.selected_objects:
        if obj.parent:
            if obj.parent.sollum_type in YMAP_ENTITY_SOLLUM_TYPES and obj.parent.type == 'EMPTY':
                objs.append(obj)
        else:
            if obj.type == 'MESH' or (obj.type == 'EMPTY' and obj.sollum_type in YMAP_ENTITY_SOLLUM_TYPES):
                objs.append(obj)
    return objs


def find_soll_ancestor(obj: Object) -> Object | None:
    """Get the parent of a Sollumz object."""
    while obj.parent:
        obj = obj.parent
        if obj.sollum_type in YMAP_ENTITY_SOLLUM_TYPES:
            if obj.parent and obj.parent.sollum_type == YMAP_ENTITY_SOLLUM_TYPES[1]:
                continue
            else:
                return obj
    return None

def find_imported_soll_root(filename: str, new_objs: list[Object]) -> Object:
    return next((x for x in new_objs if filename in x.name and
                 x.type in COMPAT_OBJECT_TYPES and
                 x.sollum_type in YMAP_ENTITY_SOLLUM_TYPES and
                 not x.parent), None)