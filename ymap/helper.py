import hashlib
from ..vicho_dependencies import dependencies_manager as dm
from .constants import entity_flags_values, map_data_flags_values, map_data_content_flags_values, entity_flags_updating, ymap_flags_updating, ymap_content_flags_updating
from bpy.types import Object

def update_entity_flags_bool_properties(self, context):
    global entity_flags_updating
    if entity_flags_updating:
        return
    entity_flags_updating = True
    for key, value in entity_flags_values.items():
        setattr(self, key, bool(self.total_flags & value))
    entity_flags_updating = False

def update_entity_flags(self, context):
    global entity_flags_updating
    if entity_flags_updating:
        return
    entity_flags_updating = True
    self.total_flags = 0
    for key, value in entity_flags_values.items():
        if getattr(self, key):
            self.total_flags |= value
    entity_flags_updating = False

def update_ymap_flags_bool_properties(self, context):
    global ymap_flags_updating
    if ymap_flags_updating:
        return
    ymap_flags_updating = True
    for key, value in map_data_flags_values.items():
        setattr(self, key, bool(self.total_flags & value))
    ymap_flags_updating = False
    
def update_ymap_flags(self, context):
    global ymap_flags_updating
    if ymap_flags_updating:
        return
    ymap_flags_updating = True
    self.total_flags = 0
    for key, value in map_data_flags_values.items():
        if getattr(self, key):
            self.total_flags |= value
    ymap_flags_updating = False
    
def update_ymap_content_flags_bool_properties(self, context):
    global ymap_content_flags_updating
    if ymap_content_flags_updating:
        return
    ymap_content_flags_updating = True
    for key, value in map_data_content_flags_values.items():
        setattr(self, key, bool(self.total_flags & value))
    ymap_content_flags_updating = False
    
def update_ymap_content_flags(self, context):
    global ymap_content_flags_updating
    if ymap_content_flags_updating:
        return
    ymap_content_flags_updating = True
    self.total_flags = 0
    for key, value in map_data_content_flags_values.items():
        if getattr(self, key):
            self.total_flags |= value
    ymap_content_flags_updating = False
    
def get_hash_from_bytes(data: bytes, algorithm:str = "sha256") -> str:
    """Returns the hash of the data"""
    hash_object = hashlib.new(algorithm)
    hash_object.update(data)
    return hash_object.hexdigest()

def resolve_hashes_from_file(file_path: str) -> None:
    all_txt_lines: list[str] = open(file_path, "r").readlines()
    for line in all_txt_lines:
        dm.JenkIndex.Ensure(line.strip())

def get_strings_loaded_count() -> int:
    return dm.JenkIndex.GetAllStrings().Length

def run_ops_without_view_layer_update(func):
    from bpy.ops import _BPyOpsSubModOp
    view_layer_update = _BPyOpsSubModOp._view_layer_update
    def dummy_view_layer_update(context):
        pass
    try:
        _BPyOpsSubModOp._view_layer_update = dummy_view_layer_update
        func()
    finally:
        _BPyOpsSubModOp._view_layer_update = view_layer_update
        
def copy_object(obj):
    new_obj = obj.copy()
    if obj.data:
        new_obj.data = obj.data.copy()
    
    for collection in obj.users_collection:
        collection.objects.link(new_obj)
    
    return new_obj


def copy_object_and_children(obj):
    new_obj = copy_object(obj)
    
    for child in obj.children:
        new_child = copy_object(child)
        new_child.parent = new_obj
        for grandchild in child.children:
            copy_object_and_children_recursive(grandchild, new_child)
    return new_obj

def copy_object_and_children_recursive(obj, parent):
    new_obj = copy_object(obj)
    new_obj.parent = parent
    for child in obj.children:
        copy_object_and_children_recursive(child, new_obj)

def get_object_from_scene(scene, obj_name: Object) -> Object:
    return scene.objects.get(obj_name)