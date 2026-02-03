from .helper import create_ymap_entities_group, create_ymap_occluders_group, create_ymap_models_occluders_group, create_ymap_box_occluders_group
from bpy.types import Object

class YmapMixin:

    """Mixin class to provide common YMAP related functionality"""

    @staticmethod
    def get_ymap(context):
        """Returns the currently selected YMAP in the scene"""
        try:
            ymap = context.scene.ymap_list[context.scene.ymap_list_index]
        except (IndexError, AttributeError):
            return None

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
    def get_ymap_occl_count(context) -> int:
        """Returns the number of occlusion culling objects in the currently selected YMAP"""
        if YmapMixin.has_occluders(context):
            return YmapMixin.get_ymap_box_occl_count(context) + YmapMixin.get_ymap_model_occl_count(context)
        return 0
    
    @staticmethod
    def get_ymap_box_occl_count(context) -> int:
        """Returns the number of box occlusion culling objects in the currently selected YMAP"""
        ymap = YmapMixin.get_ymap(context)
        if ymap and ymap.ymap_box_occluders:
            return len(ymap.ymap_box_occluders)
        return 0
    
    @staticmethod
    def get_box_occl(context) -> Object | None:
        """Returns the box occlusion culling object by index in the currently selected YMAP"""
        ymap = YmapMixin.get_ymap(context)
        if ymap and ymap.ymap_box_occluders:
            return ymap.ymap_box_occluders[YmapMixin.get_ymap_box_occl_index(context)]
        return None
    
    @staticmethod
    def get_ymap_box_occl_index(context) -> int:
        """Returns the index of the currently selected box occlusion culling object in the currently selected YMAP"""
        ymap = YmapMixin.get_ymap(context)
        if ymap and ymap.ymap_box_occluders:
            return ymap.ymap_box_occluders_index
        return 0
    
    @staticmethod
    def get_ymap_occl_group_obj(context) -> Object:
        """Returns the YMAP entities group object, creates it if it doesn't exist"""
        ymap_obj: Object = YmapMixin.get_ymap_obj(context)
        return next((ent_group for ent_group in ymap_obj.children
                     if ent_group.vicho_type == "vicho_ymap_occluder_base"), None) or create_ymap_occluders_group(ymap_obj)
    @staticmethod
    def get_ymap_box_occl_group_obj(context) -> Object:
        """Returns the YMAP entities group object, creates it if it doesn't exist"""
        ymap_occl_obj = YmapMixin.get_ymap_occl_group_obj(context)
        return next((ent_group for ent_group in ymap_occl_obj.children
                     if ent_group.vicho_type == "vicho_ymap_box_occluders"), None) or create_ymap_box_occluders_group(ymap_occl_obj)
    
    @staticmethod
    def get_ymap_model_occl_group_obj(context) -> Object:
        """Returns the YMAP entities group object, creates it if it doesn't exist"""
        ymap_occl_obj = YmapMixin.get_ymap_occl_group_obj(context)
        return next((ent_group for ent_group in ymap_occl_obj.children
                     if ent_group.vicho_type == "vicho_ymap_model_occluders"), None) or create_ymap_models_occluders_group(ymap_occl_obj)
    
    @staticmethod
    def get_ymap_model_occl_count(context) -> int:
        """Returns the number of model occlusion culling objects in the currently selected YMAP"""
        ymap = YmapMixin.get_ymap(context)
        if ymap and ymap.ymap_model_occluders:
            return len(ymap.ymap_model_occluders)
        return 0
    
    
    @staticmethod
    def get_model_occl(context) -> Object:
        """Returns the model occlusion culling object by index in the currently selected YMAP"""
        ymap = YmapMixin.get_ymap(context)
        if ymap and ymap.ymap_model_occluders:
            return ymap.ymap_model_occluders[YmapMixin.get_ymap_model_occl_index(context)]
        return None
    
    @staticmethod
    def get_ymap_model_occl_index(context) -> int:
        """Returns the index of the currently selected model occlusion culling object in the currently selected YMAP"""
        ymap = YmapMixin.get_ymap(context)
        if ymap and ymap.ymap_model_occluders:
            return ymap.ymap_model_occluders_index
        return 0
    
    @staticmethod
    def has_occluders(context) -> bool:
        """Returns True if the current YMAP has occlusion culling objects"""
        return YmapMixin.get_ymap_occl_count(context) > 0
    
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
    def has_entities(context) -> bool:
        """Returns True if the current YMAP has entities"""
        return YmapMixin.get_ymap_ent_count(context) > 0
    
    @staticmethod
    def has_physics_dictionaries(context):
        """Returns True if the current YMAP has physicsDictionary"""
        return YmapMixin.get_ymap_phys_dict_count(context) > 0

    @staticmethod
    def set_ent_idx(context, index) -> None:
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