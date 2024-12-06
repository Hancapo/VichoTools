from ..vicho_dependencies import dependencies_manager as dm
from pathlib import Path
from .helper import get_hash_from_bytes
import bpy
from .constants import COMPAT_SOLL_TYPES, OBJECT_TYPES
from bpy.types import Object, Scene

def get_ymap_name(ymap) -> str:
    """Returns the name of the YMAP"""
    return ymap.CMapData.name.ToString()

def get_ymap_parent(ymap) -> str:
    """Returns the parent of the YMAP"""
    return ymap.CMapData.parent.ToString()

def get_ymap_flags(ymap) -> int:
    """Returns the flags of the YMAP"""
    return ymap.CMapData.flags

def get_ymap_content_flags(ymap) -> int:
    """Returns the content flags of the YMAP"""
    return ymap.CMapData.contentFlags

def get_ymap_streaming_extents_min(ymap) -> tuple[float, float, float]:
    """Returns the streaming extents min of the YMAP"""
    return (ymap.CMapData.streamingExtentsMin.X, ymap.CMapData.streamingExtentsMin.Y, ymap.CMapData.streamingExtentsMin.Z)

def get_ymap_streaming_extents_max(ymap) -> tuple[float, float, float]:
    """Returns the streaming extents max of the YMAP"""
    return (ymap.CMapData.streamingExtentsMax.X, ymap.CMapData.streamingExtentsMax.Y, ymap.CMapData.streamingExtentsMax.Z)

def get_ymap_entities_extents_min(ymap) -> tuple[float, float, float]:
    """Returns the entities extents min of the YMAP"""
    return (ymap.CMapData.entitiesExtentsMin.X, ymap.CMapData.entitiesExtentsMin.Y, ymap.CMapData.entitiesExtentsMin.Z)

def get_ymap_entities_extents_max(ymap) -> tuple[float, float, float]:
    """Returns the entities extents max of the YMAP"""
    return (ymap.CMapData.entitiesExtentsMax.X, ymap.CMapData.entitiesExtentsMax.Y, ymap.CMapData.entitiesExtentsMax.Z)

def ymap_exist_in_scene(scene: Scene, new_ymap: str) -> bool:
    """Checks if a YMAP already exists in the scene"""
    p: Path = Path(new_ymap)
    new_ymap_bytes: bytes = p.read_bytes()
    new_ymap_bytes_hash: str = get_hash_from_bytes(new_ymap_bytes)
    ymap_list = scene.fake_ymap_list
    if len(ymap_list) > 0:
        for ymap in ymap_list:
            print(f"YMAP HASH: {ymap.hash} NEW HASH: {new_ymap_bytes_hash}")
            if ymap.hash == new_ymap_bytes_hash:
                return True
    return False
            
def add_ymap_to_scene(scene: Scene, new_ymap_path: str, i_ents: bool, i_occls: bool, i_timemods: bool, i_cargens: bool, self, assets_path: str = None) -> bool:
    p: Path = Path(new_ymap_path)
    filename = p.stem
    if not ymap_exist_in_scene(scene, new_ymap_path):
        if dm.add_ymap(new_ymap_path):
            scene.fake_ymap_list.add()
            current_index = len(scene.fake_ymap_list) - 1
            fill_data_from_ymap(scene, current_index)
            if i_ents and assets_path is not None:
                import_entity_objs(scene, current_index, assets_path, self)
            self.report({'INFO'}, f"YMAP {filename} added to scene")
            return True
        else:
            self.report({'ERROR'}, f"Error adding YMAP {filename} to scene")
            return False
    else:
        self.report({'ERROR'}, f"YMAP {filename} already exists in scene")
        return False
 
def remove_ymap_from_scene(scene: Scene, index: int) -> bool:
    """Removes a YMAP from the scene"""
    if dm.remove_ymap(index):
        scene.fake_ymap_list.remove(index)
        scene.ymap_list_index = len(scene.fake_ymap_list) - 1
        return True
    return False
    
def fill_data_from_ymap(scene: Scene, index: int) -> None:
    """Fills the data from the selected YMAP"""
    current_ymap = dm.get_ymap(index)
    current_ymap_bytes = dm.get_ymap_bytes(index)
    any_entities = any_entity_exist_in_ymap(current_ymap)
    scene.fake_ymap_list[index].name = get_ymap_name(current_ymap)
    scene.fake_ymap_list[index].parent = get_ymap_parent(current_ymap)
    scene.fake_ymap_list[index].flags.total_flags = get_ymap_flags(current_ymap)
    scene.fake_ymap_list[index].content_flags.total_flags = get_ymap_content_flags(current_ymap)
    scene.fake_ymap_list[index].streaming_extents_min = get_ymap_streaming_extents_min(current_ymap)
    scene.fake_ymap_list[index].streaming_extents_max = get_ymap_streaming_extents_max(current_ymap)
    scene.fake_ymap_list[index].entities_extents_min = get_ymap_entities_extents_min(current_ymap)
    scene.fake_ymap_list[index].entities_extents_max = get_ymap_entities_extents_max(current_ymap)
    scene.fake_ymap_list[index].hash = get_hash_from_bytes(current_ymap_bytes)
    scene.fake_ymap_list[index].any_entities = any_entities
    if any_entities:
        for ent in get_all_entities_from_ymap(current_ymap):
            new_entity = scene.fake_ymap_list[index].entities.add()
            new_entity.archetype_name = ent._CEntityDef.archetypeName.ToString()
            new_entity.flags.total_flags = ent._CEntityDef.flags
            new_entity.guid = str(ent._CEntityDef.guid)
            new_entity.position = (ent._CEntityDef.position.X, ent._CEntityDef.position.Y, ent._CEntityDef.position.Z)
            new_entity.rotation = (ent._CEntityDef.rotation.W, ent._CEntityDef.rotation.X, ent._CEntityDef.rotation.Y, -ent._CEntityDef.rotation.Z)
            new_entity.scale_xy = ent._CEntityDef.scaleXY
            new_entity.scale_z = ent._CEntityDef.scaleZ
            new_entity.parent_index = ent._CEntityDef.parentIndex
            new_entity.lod_distance = ent._CEntityDef.lodDist
            new_entity.child_lod_distance = ent._CEntityDef.childLodDist
            new_entity.num_children = ent._CEntityDef.numChildren
            new_entity.lod_level = get_entity_lod_level(ent)
            new_entity.priority_level = ent._CEntityDef.priorityLevel.ToString()
            new_entity.ambient_occlusion_multiplier = ent._CEntityDef.ambientOcclusionMultiplier
            new_entity.artificial_ambient_occlusion = ent._CEntityDef.artificialAmbientOcclusion
            new_entity.tintValue = ent._CEntityDef.tintValue
            new_entity.type = get_entity_type(ent)
            if get_entity_is_mlo_instance(ent):
                new_entity.is_mlo_instance = True

def import_entity_objs(scene: Scene, index: int, asset_path: str, self) -> None:
    current_ymap = scene.fake_ymap_list[index]
    ents: str = current_ymap.entities
    for e in ents:
        p: Path = Path(asset_path)
        xml_file = f"{e.archetype_name}.ydr.xml" if Path.exists(p / f"{e.archetype_name}.ydr.xml") else f"{e.archetype_name}.yft.xml"
        before_import = set(bpy.data.objects.keys())
        if Path.exists(p / xml_file):
            bpy.ops.sollumz.import_assets(directory=str(p), files=[{"name": xml_file}])
            after_import = set(bpy.data.objects.keys())
            new_objs_names = after_import - before_import
            new_objs = [bpy.data.objects[name] for name in new_objs_names]
            imported_obj: Object = get_obj_soll_parent(e.archetype_name, new_objs)
            apply_transforms_to_obj_from_entity(imported_obj, e)
                

def get_obj_soll_parent(filename: str, new_objs: list[Object]) -> Object:
    return next((x for x in new_objs if filename in x.name and
                 x.type in OBJECT_TYPES and
                 x.sollum_type in COMPAT_SOLL_TYPES and
                 not x.parent), None)


def import_asset_by_name(scene: Scene, newPath: str, filename: str, before_import) -> None:
    pass

def apply_transforms_to_obj_from_entity(obj:Object, entity) -> None:
    if obj is not None:
        entity.linked_object = obj
        entity.linked_object.location = entity.position
        entity.linked_object.rotation_mode = 'QUATERNION'
        entity.linked_object.rotation_quaternion = entity.rotation
        entity.linked_object.scale = (entity.scale_xy, entity.scale_xy, entity.scale_z)
        
def any_entity_exist_in_ymap(ymap) -> bool:
    """Checks if any entity exists in the YMAP"""
    return ymap.AllEntities is not None

def get_all_entities_from_ymap(ymap) -> list:
    """Returns all the entities from the YMAP"""
    return ymap.AllEntities

def get_entity_type(entity) -> str:
    """Returns the entity type"""
    return "ENTITY" if entity.MloInstance is None else "MLOINSTANCE"

def get_entity_lod_level(entity) -> str:
    """Returns the LOD level of the entity"""
    return str(entity._CEntityDef.lodLevel.ToString())

def get_entity_is_mlo_instance(entity) -> bool:
    """Returns if the entity is a MLO instance"""
    return entity.IsMlo