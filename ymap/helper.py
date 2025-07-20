import hashlib
from ..vicho_dependencies import dependencies_manager as dm
from .constants import entity_flags_values, map_data_flags_values, map_data_content_flags_values, entity_flags_updating, ymap_flags_updating, ymap_content_flags_updating
from bpy.types import Object, Context
from pathlib import Path
import bpy

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

def str_loaded_count() -> int:
    if dm.available:
        return dm.JenkIndex.GetAllStrings().Length
    else:
        return None

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
        
def instance_obj(obj: Object) -> Object:
    new_obj: Object = obj.copy()
    if obj.data:
        new_obj.data = obj.data
    for collection in obj.users_collection:
        collection.objects.link(new_obj)
    return new_obj

def instance_obj_and_child(obj: Object) -> Object:
    new_obj: Object = instance_obj(obj)
    
    for child in obj.children:
        new_child = instance_obj(child)
        new_child.parent = new_obj
        for grandchild in child.children:
            instance_obj_and_child_recur(grandchild, new_child)
    return new_obj

def instance_obj_and_child_recur(obj: Object, parent: Object):
    new_obj: Object = instance_obj(obj)
    new_obj.parent = parent
    for child in obj.children:
        instance_obj_and_child_recur(child, new_obj)

def get_obj_from_scene(scene, obj_name: Object) -> Object:
    return scene.objects.get(obj_name)

def get_bytes_from_file(file_path: str) -> bytes:
    return bytes(dm.File.ReadAllBytes(file_path))

def get_fn_wt_ext(file_path: str) -> str:
    return Path(file_path).stem

def get_scene_collection(scene) -> str:
    """Returns the name of the scene collection"""
    return scene.collection.name if scene.collection else "Scene Collection"

def update_entity_index(self, context: Context):
    unselect_entities_from_all_ymaps(context)
    entity_idx = self.entity_list_index
    selected_ymap = context.scene.ymap_list[context.scene.ymap_list_index]
    selected_ymap.entities[entity_idx].linked_object.select_set(True)
    

def unselect_entities_from_all_ymaps(context: Context):
    """Unselects all entities from all YMAPs in the scene"""
    for ymap in context.scene.ymap_list:
        if ymap.entities:
            for entity in ymap.entities:
                entity.linked_object.select_set(False)
                
def set_sollumz_export_settings() -> None:
    """Sets the proper settings needed for assets export"""
    loaded_addons = bpy.context.preferences.addons
    preferences = None
    for addon in loaded_addons:
        if "sollumz" in addon.module:
            preferences = loaded_addons[addon.module].preferences
            break
    preferences.export_settings.limit_to_selected = True            

def change_ent_parenting(objs: list[Object], do_parent = False):
    """Changes the parenting of the selected objects to the YMAP entities group"""
    scene = bpy.context.scene
    ymap_obj = scene.ymap_list[scene.ymap_list_index].ymap_object
    ymap_ent_group_obj = next((obj for obj in ymap_obj.children if obj.vicho_type == "vicho_ymap_entities"), None)
    bpy.ops.object.select_all(action='DESELECT')
    if ymap_ent_group_obj:
        for obj in objs:
            obj.select_set(True)
            if do_parent:
                obj.parent = ymap_ent_group_obj
            else:
                obj.parent = None

