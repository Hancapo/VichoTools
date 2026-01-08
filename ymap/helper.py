import hashlib

from ..misc.funcs import create_ymap_entities_group
from ..vicho_dependencies import dependencies_manager as dm
from .constants import (ENTITY_FLAGS_VALUES,
                        MAP_DATA_FLAGS_VALUES, 
                        MAP_DATA_CONTENT_FLAGS_VALUES, 
                        ENTITY_FLAGS_UPDATING, 
                        YMAP_FLAGS_UPDATING, 
                        YMAP_CONTENT_FLAGS_UPDATING,
                        COMPAT_SOLL_TYPES,
                        MAPENTITY_FLAGS)
from bpy.types import Object, Context
from pathlib import Path
import bpy

_is_updating_entity_prop:bool = False

class YmapMixin:
    
    """Mixin class to provide common YMAP related functionality"""
    
    @staticmethod
    def get_ymap(context):
        """Returns the currently selected YMAP in the scene"""
        ymap = context.scene.ymap_list[context.scene.ymap_list_index]
        if ymap:
            return ymap
        return None

    @staticmethod
    def set_ymap_index(context, index) -> None:
        """Sets the selected YMAP by index"""
        context.scene.ymap_list_index = index

    @staticmethod
    def get_ymap_obj(context) -> Object:
        """Returns the YMAP empty object of the currently selected YMAP"""
        if YmapMixin.get_ymap(context):
            return YmapMixin.get_ymap(context).ymap_object

    @staticmethod
    def get_ymap_ent_group_obj(context) -> Object:
        """Returns the YMAP entities group object, creates it if it doesn't exist"""
        ymap_obj = YmapMixin.get_ymap_obj(context)
        return next((ent_group for ent_group in ymap_obj.children 
                     if ent_group.vicho_type == "vicho_ymap_entities"), None) or create_ymap_entities_group(ymap_obj)
        
    @staticmethod
    def get_ymap_ent_count(context) -> int:
        """Returns the number of entities in the currently selected YMAP"""
        ymap = YmapMixin.get_ymap(context)
        if ymap and ymap.entities:
            return len(ymap.entities)
        return 0
    
    @staticmethod
    def get_ymap_phys_dict_count(context) -> int:
        """Returns the number of physics dictionaries in the currently selected YMAP"""
        ymap = YmapMixin.get_ymap(context)
        if ymap and ymap.ymap_phys_dicts:
            return len(ymap.ymap_phys_dicts)
        return 0

    @staticmethod
    def get_ymap_count(context):
        """Returns the number of YMAPs in the scene"""
        return len(context.scene.ymap_list) if context.scene.ymap_list else 0

    @staticmethod
    def get_ent(context):
        """Returns the currently selected entity in the current YMAP"""
        ymap = YmapMixin.get_ymap(context)
        if ymap and ymap.entities:
            return ymap.entities[context.scene.entity_list_index]
        return None
    
    @staticmethod
    def get_ent_by_index(context, index):
        """Returns the currently selected entity in the current YMAP by index"""
        ymap = YmapMixin.get_ymap(context)
        if ymap and ymap.entities and index < len(ymap.entities):
            return ymap.entities[index]
        return None

    @staticmethod
    def has_entities(context):
        """Returns True if the current YMAP has entities"""
        return YmapMixin.get_ymap_ent_count(context) > 0

    @staticmethod
    def set_ent_idx(context, index):
        """Sets the selected entity by index in the current YMAP"""
        context.scene.entity_list_index = index
    
    @staticmethod
    def get_ent_from_viewport_select(context, obj) -> tuple[Object, int, Object, int] | None:
        """Returns the entity and its index from the selected object, along with the YMAP and its index"""
        for i_y, ymap in enumerate(context.scene.ymap_list):
            for i_e, ent in enumerate(ymap.entities):
                if ent.linked_object == obj:
                    return ent, i_e, ymap, i_y
        return None
    
    @staticmethod
    def toggle_ent_visibility(visibility, entity) -> None:
        """Toggles the visibility of the currently selected entity"""
        linked_obj: Object = entity.linked_object
        if entity and linked_obj:
            linked_obj.hide_set(not visibility)
            if linked_obj.children:
                for child in linked_obj.children_recursive:
                    child.hide_set(not visibility)
                    
    @staticmethod
    def get_filtered_entities_idx(context, filter_string: str) -> list[int]:
        """Returns a list of indices of entities that match the filter string"""
        ymap = YmapMixin.get_ymap(context)
        if ymap and ymap.entities and filter_string:
            return [i for i, ent in enumerate(ymap.entities) if filter_string in ent.archetype_name.lower()]
        return []
    
    @staticmethod
    def clear_entities_selection(context) -> None:
        """Clears the selection of all entities in the current YMAP"""
        ymap = YmapMixin.get_ymap(context)
        if ymap and ymap.entities:
            for ent in ymap.entities:
                ent.is_multi_selected = False

    @staticmethod
    def execute_menu_op(context, op_id):
        """Executes a menu operation by setting the active category in the YMAP"""
        ymap = YmapMixin.get_ymap(context)
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

def update_flags_on_entities(self, context, prop_name: str) -> None:
    update_entity_flags_bool_properties(self, context)
    update_entity_prop_value(self, context, prop_name)

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
        self.linked_object.parent = YmapMixin.get_ymap_ent_group_obj(context)
        if self.linked_object.sollum_type == "sollumz_bound_composite":
            entity = YmapMixin.get_ent(context)
            entity.sollum_type = "sollumz_bound_composite"
            entity.is_mlo_instance = True
            
def get_entity_sets_from_entity(context) -> list[str]:
    """Returns the entity sets from the entity's MLO archetype definition"""
    entity = YmapMixin.get_ent(context)
    linked_obj: Object = entity.linked_object
    
    for ytyp in context.scene.ytyps:
        for arch in ytyp.archetypes:
            if arch.type == "sollumz_archetype_mlo" and arch.name == linked_obj.name:
                return [es.name for es in arch.entity_sets]
    return []

def get_sel_objs_list(context: Context) -> list[Object]:
    """Returns a list of selected objects in the context"""
    objs: list[Object] = []
    for obj in context.selected_objects:
        if obj.parent:
            if obj.parent.sollum_type in COMPAT_SOLL_TYPES and obj.parent.type == 'EMPTY':
                objs.append(obj)
        else:
            if obj.type == 'MESH' or (obj.type == 'EMPTY' and obj.sollum_type in COMPAT_SOLL_TYPES):
                objs.append(obj)
    return objs

def update_entity_prop_value(self, context, prop_name: str) -> None:
    """Updates the property value"""
    global _is_updating_entity_prop
    
    if _is_updating_entity_prop:
        return
    
    match prop_name:
        case "is_visible":
            try:
                ymap = YmapMixin.get_ymap(context)
                if ymap.entity_multi_select:
                    _is_updating_entity_prop = True
                    for idx in ymap["selected_entity_index"]:
                        ent = YmapMixin.get_ent_by_index(context, idx)
                        if ent:
                            ent.is_visible = self.is_visible
                            YmapMixin.toggle_ent_visibility(self.is_visible, ent)
                else:
                    _is_updating_entity_prop = True
                    YmapMixin.toggle_ent_visibility(self.is_visible, self)
            finally:
                _is_updating_entity_prop = False
        case "lod_distance":
            try:
                #print(f"Updating LOD distance to {self.lod_distance}")
                ymap = YmapMixin.get_ymap(context)
                if ymap.entity_multi_select:
                    _is_updating_entity_prop = True
                    for idx in ymap["selected_entity_index"]:
                        ent = YmapMixin.get_ent_by_index(context, idx)
                        if ent:
                            ent.lod_distance = self.lod_distance
            finally:
                _is_updating_entity_prop = False
        case "total_flags":
            try:
                entity_data_str: str = self.path_from_id().rsplit(".", 1)[0]
                ymap = self.id_data.path_resolve(entity_data_str.rsplit(".", 1)[0])
                if ymap.entity_multi_select:
                    _is_updating_entity_prop = True
                    for idx in ymap["selected_entity_index"]:
                        ent = YmapMixin.get_ent_by_index(context, idx)
                        if ent:
                            ent.flags.total_flags = self.total_flags
            finally:
                _is_updating_entity_prop = False
        case "is_marked":
            try:
                ymap = YmapMixin.get_ymap(context)
                if ymap.entity_multi_select:
                    _is_updating_entity_prop = True
                    for idx in ymap["selected_entity_index"]:
                        ent = YmapMixin.get_ent_by_index(context, idx)
                        if ent:
                            ent.is_mesh_edited = self.is_mesh_edited
            finally:
                _is_updating_entity_prop = False
        case _:
            pass

VALID_MAPDATA_ENTITY_FLAGS = sum(int(i[0]) for i in MAPENTITY_FLAGS)

def enum_to_mask(enum_set):
    return sum(int(x) for x in enum_set)

def mask_to_enum(mask: int):
    out = set()
    for ident, _name, _desc in MAPENTITY_FLAGS:
        bit = int(ident)
        if mask & bit:
            out.add(ident)
    return out

def get_mask(self) -> int:
    return enum_to_mask(self.flags)

def set_mask(self, value: int) -> None:
    m = int(value) & VALID_MAPDATA_ENTITY_FLAGS
    self.flags = mask_to_enum(m)