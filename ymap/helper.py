import hashlib

from ..misc.funcs import create_ymap_entities_group
from ..vicho_dependencies import dependencies_manager as dm
from .constants import (ENTITY_FLAGS_VALUES,
                        MAP_DATA_FLAGS_VALUES, 
                        MAP_DATA_CONTENT_FLAGS_VALUES, 
                        ENTITY_FLAGS_UPDATING, 
                        YMAP_FLAGS_UPDATING, 
                        YMAP_CONTENT_FLAGS_UPDATING)
from bpy.types import Object, Context
from pathlib import Path
import bpy

class YmapData:
    def get_ymap(self, context):
        ymap = context.scene.ymap_list[context.scene.ymap_list_index]
        if ymap:
            return ymap
        return None
    
    def get_ymap_obj(self, context):
        if self.get_ymap(context):
            return self.get_ymap(context).ymap_object
        
    def get_ymap_ent_group_obj(self, context):
        ymap_obj = self.get_ymap_obj(context)
        return next((ent_group for ent_group in ymap_obj.children if ent_group.vicho_type == "vicho_ymap_entities"), None) or create_ymap_entities_group(ymap_obj)
    
    def get_ent(self, context):
        ymap = self.get_ymap(context)
        if ymap and ymap.entities:
            return ymap.entities[context.scene.entity_list_index]
        return None
    
    def execute_menu_op(self, context, op_id):
        ymap = self.get_ymap(context)
        if ymap:
            ymap.active_category = op_id
            return {"FINISHED"}

def update_entity_flags_bool_properties(self, context):
    global ENTITY_FLAGS_UPDATING
    if ENTITY_FLAGS_UPDATING:
        return
    ENTITY_FLAGS_UPDATING = True
    for key, value in ENTITY_FLAGS_VALUES.items():
        setattr(self, key, bool(self.total_flags & value))
    ENTITY_FLAGS_UPDATING = False

def update_entity_flags(self, context):
    global ENTITY_FLAGS_UPDATING
    if ENTITY_FLAGS_UPDATING:
        return
    ENTITY_FLAGS_UPDATING = True
    self.total_flags = 0
    for key, value in ENTITY_FLAGS_VALUES.items():
        if getattr(self, key):
            self.total_flags |= value
    ENTITY_FLAGS_UPDATING = False

def update_ymap_flags_bool_properties(self, context):
    global YMAP_FLAGS_UPDATING
    if YMAP_FLAGS_UPDATING:
        return
    YMAP_FLAGS_UPDATING = True
    for key, value in MAP_DATA_FLAGS_VALUES.items():
        setattr(self, key, bool(self.total_flags & value))
    YMAP_FLAGS_UPDATING = False
    
def update_ymap_flags(self, context):
    global YMAP_FLAGS_UPDATING
    if YMAP_FLAGS_UPDATING:
        return
    YMAP_FLAGS_UPDATING = True
    self.total_flags = 0
    for key, value in MAP_DATA_FLAGS_VALUES.items():
        if getattr(self, key):
            self.total_flags |= value
    YMAP_FLAGS_UPDATING = False
    
def update_ymap_content_flags_bool_properties(self, context):
    global YMAP_CONTENT_FLAGS_UPDATING
    if YMAP_CONTENT_FLAGS_UPDATING:
        return
    YMAP_CONTENT_FLAGS_UPDATING = True
    for key, value in MAP_DATA_CONTENT_FLAGS_VALUES.items():
        setattr(self, key, bool(self.total_flags & value))
    YMAP_CONTENT_FLAGS_UPDATING = False
    
def update_ymap_content_flags(self, context):
    global YMAP_CONTENT_FLAGS_UPDATING
    if YMAP_CONTENT_FLAGS_UPDATING:
        return
    YMAP_CONTENT_FLAGS_UPDATING = True
    self.total_flags = 0
    for key, value in MAP_DATA_CONTENT_FLAGS_VALUES.items():
        if getattr(self, key):
            self.total_flags |= value
    YMAP_CONTENT_FLAGS_UPDATING = False
    
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

def run_ops_without_view_layer_update(func) -> None:
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

def unselect_entities_from_all_ymaps(context: Context) -> None:
    """Unselects all entities from all YMAPs in the scene"""
    for ymap in context.scene.ymap_list:
        if ymap.entities:
            for entity in ymap.entities:
                entity.linked_object.select_set(False)
                
def get_sollumz_settings() -> bpy.types.AddonPreferences:
    """Returns the Sollumz addon preferences"""
    loaded_addons = bpy.context.preferences.addons
    for addon in loaded_addons:
        if "sollumz" in addon.module:
            return loaded_addons[addon.module].preferences
    return None
                
def set_sollumz_export_settings() -> None:
    """Sets the proper settings needed for assets export"""
    preferences = get_sollumz_settings()
    if preferences:
        preferences.export_settings.limit_to_selected = True

def change_ent_parenting(objs: list[Object], do_parent = False) -> None:
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

def update_linked_obj(self, context) -> None:
    """Updates the linked object for the entity"""
    if not self.linked_object:
        return
    if not self.linked_object.parent:
        self.linked_object.parent = YmapData.get_ymap_ent_group_obj(context)
        if self.linked_object.sollum_type == "sollumz_bound_composite":
            entity = YmapData.get_ent(context)
            entity.sollum_type = "sollumz_bound_composite"
            entity.is_mlo_instance = True
            
def get_entity_sets_from_entity(self, context) -> list[str]:
    """Returns the entity sets from the entity's MLO archetype definition"""
    entity = YmapData.get_ent(self, context)
    linked_obj: Object = entity.linked_object
    
    for ytyp in context.scene.ytyps:
        for arch in ytyp.archetypes:
            if arch.type == "sollumz_archetype_mlo" and arch.name == linked_obj.name:
                return [es.name for es in arch.entity_sets]
    return []