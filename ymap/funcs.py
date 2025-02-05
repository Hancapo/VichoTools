from ..vicho_dependencies import dependencies_manager as d
from pathlib import Path
from .helper import run_ops_without_view_layer_update, instance_obj_and_child, get_obj_from_scene, get_fn_wt_ext
import bpy
from .constants import COMPAT_SOLL_TYPES, OBJECT_TYPES
from bpy.types import Object, Scene

def get_name(ymap) -> str:
    """Returns the name of the YMAP"""
    return ymap.CMapData.name.ToString()

def get_parent(ymap) -> str:
    """Returns the parent of the YMAP"""
    return ymap.CMapData.parent.ToString()

def get_flags(ymap) -> int:
    """Returns the flags of the YMAP"""
    return ymap.CMapData.flags

def get_content_flags(ymap) -> int:
    """Returns the content flags of the YMAP"""
    return ymap.CMapData.contentFlags

def get_streaming_extents_min(ymap) -> tuple[float, float, float]:
    """Returns the streaming extents min of the YMAP"""
    return (ymap.CMapData.streamingExtentsMin.X, ymap.CMapData.streamingExtentsMin.Y, ymap.CMapData.streamingExtentsMin.Z)

def get_streaming_extents_max(ymap) -> tuple[float, float, float]:
    """Returns the streaming extents max of the YMAP"""
    return (ymap.CMapData.streamingExtentsMax.X, ymap.CMapData.streamingExtentsMax.Y, ymap.CMapData.streamingExtentsMax.Z)

def get_ents_extents_min(ymap) -> tuple[float, float, float]:
    """Returns the entities extents min of the YMAP"""
    return (ymap.CMapData.entitiesExtentsMin.X, ymap.CMapData.entitiesExtentsMin.Y, ymap.CMapData.entitiesExtentsMin.Z)

def get_ents_extents_max(ymap) -> tuple[float, float, float]:
    """Returns the entities extents max of the YMAP"""
    return (ymap.CMapData.entitiesExtentsMax.X, ymap.CMapData.entitiesExtentsMax.Y, ymap.CMapData.entitiesExtentsMax.Z)

def ymap_exist_in_scene(scene: Scene, new_ymap: str) -> bool:
    """Checks if a YMAP already exists in the scene"""
    fn: str = get_fn_wt_ext(new_ymap)
    ymap_list = scene.ymap_list
    if len(ymap_list) > 0:
        for ymap in ymap_list:
            if ymap.name == fn:
                return True
    return False

            
def import_ymap_to_scene(scene: Scene, new_ymap_path: str, i_ents: bool, i_occls: bool, i_timemods: bool, i_cargens: bool, do_props: bool, self, assets_path: str = None) -> bool:
    p: Path = Path(new_ymap_path)
    filename = p.stem
    if not ymap_exist_in_scene(scene, new_ymap_path):
        scene.ymap_list.add()
        current_index = len(scene.ymap_list) - 1
        ymap = get_ymap_from_file(new_ymap_path)
        fill_map_data_from_ymap(scene, current_index, ymap, do_props)
        if i_ents and assets_path is not None:
            import_ent_objs(scene, current_index, assets_path, self)
        self.report({'INFO'}, f"YMAP {filename} added to scene")
        return True
    else:
        self.report({'ERROR'}, f"YMAP {filename} already exists in scene")
        return False
 
def remove_ymap_from_scene(scene: Scene, index: int) -> bool:
    """Removes a YMAP from the scene"""
    scene.ymap_list.remove(index)
    scene.ymap_list_index = len(scene.ymap_list) - 1
    return True

def add_ymap_to_scene(scene: Scene) -> None:
    """Adds a YMAP to the scene"""
    scene.ymap_list.add()
    scene.ymap_list_index = len(scene.ymap_list) + 1
    
def fill_map_data_from_ymap(scene: Scene, index: int, current_ymap, do_props: bool) -> None:
    """Fills the data from the selected YMAP"""
    any_entities = any_ent_exists_in_ymap(current_ymap)
    scene.ymap_list[index].name = get_name(current_ymap)
    scene.ymap_list[index].parent = get_parent(current_ymap)
    scene.ymap_list[index].flags.total_flags = get_flags(current_ymap)
    scene.ymap_list[index].content_flags.total_flags = get_content_flags(current_ymap)
    scene.ymap_list[index].streaming_extents_min = get_streaming_extents_min(current_ymap)
    scene.ymap_list[index].streaming_extents_max = get_streaming_extents_max(current_ymap)
    scene.ymap_list[index].entities_extents_min = get_ents_extents_min(current_ymap)
    scene.ymap_list[index].entities_extents_max = get_ents_extents_max(current_ymap)
    scene.ymap_list[index].any_entities = any_entities
    fill_ents_data_from_ymap(scene, index, current_ymap, any_entities, do_props)
        

def fill_ents_data_from_ymap(scene: Scene, index: int, current_ymap, any_ents: bool, do_props: bool) -> None:
    """Fills the entity data from the selected YMAP"""
    if any_ents:
        for ent in get_all_ents_from_ymap(current_ymap):
            if not do_props and get_ent_lod_level(ent) == "LODTYPES_DEPTH_ORPHANHD":
                continue
            new_entity = scene.ymap_list[index].entities.add()
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
            new_entity.lod_level = ent._CEntityDef.lodLevel.ToString()
            new_entity.priority_level = ent._CEntityDef.priorityLevel.ToString()
            new_entity.ambient_occlusion_multiplier = ent._CEntityDef.ambientOcclusionMultiplier
            new_entity.artificial_ambient_occlusion = ent._CEntityDef.artificialAmbientOcclusion
            new_entity.tintValue = ent._CEntityDef.tintValue
            new_entity.type = get_ent_type(ent)
            new_entity.is_mlo_instance = is_mlo_instance(ent)
    

def import_ent_objs(scene: Scene, index: int, asset_path: str, self) -> None:
    entities = scene.ymap_list[index].entities
    for e in entities:
        p: Path = Path(asset_path)
        xml_file: str = f"{e.archetype_name}.ydr.xml" if Path.exists(p / f"{e.archetype_name}.ydr.xml") else f"{e.archetype_name}.yft.xml"
        before_import: set[str] = set(bpy.data.objects.keys())
        if Path.exists(p / xml_file):
            working_obj: Object = None
            if not get_obj_from_scene(scene, e.archetype_name):
                def fast_import():
                    bpy.ops.sollumz.import_assets(directory=str(p), files=[{"name": xml_file}])
                run_ops_without_view_layer_update(fast_import)
                working_obj = get_imported_asset(before_import, e)
            else:
                existing_obj = get_obj_from_scene(scene, e.archetype_name)
                if existing_obj is not None:
                    working_obj = instance_obj_and_child(existing_obj)
            
            apply_transforms_to_obj_from_entity(working_obj, e)

def get_obj_soll_parent(filename: str, new_objs: list[Object]) -> Object:
    return next((x for x in new_objs if filename in x.name and
                 x.type in OBJECT_TYPES and
                 x.sollum_type in COMPAT_SOLL_TYPES and
                 not x.parent), None)

def get_imported_asset(before_import, entity, purify = True) -> None:
    after_import: set[str] = set(bpy.data.objects.keys())
    new_objs_names: set[str] = after_import - before_import
    new_objs: list[object] = [bpy.data.objects[name] for name in new_objs_names]
    imported_obj: Object = get_obj_soll_parent(entity.archetype_name, new_objs)
    return imported_obj

def get_purified_asset(obj: Object) -> Object:
    match obj.sollum_type:
        case "sollumz_drawable":
            
            pass
        case "sollumz_fragment":
            pass
        case _:
            pass
        
def delete_all_cols(obj: Object) -> None:
    pass

def delete_all_lights(obj: Object) -> None:
    pass

def remove_non_high_meshes(obj: Object) -> None:
    obj.sz_lods.very_low.mesh = None
    obj.sz_lods.low.mesh = None
    obj.sz_lods.medium.mesh = None
    obj.sz_lods.very_high.mesh = None

def apply_transforms_to_obj_from_entity(obj:Object, entity) -> None:
    """Applies the transforms from the entity to the object"""
    if obj is not None:
        entity.linked_object = obj
        entity.linked_object.location = entity.position
        entity.linked_object.rotation_mode = 'QUATERNION'
        entity.linked_object.rotation_quaternion = entity.rotation
        entity.linked_object.scale = (entity.scale_xy, entity.scale_xy, entity.scale_z)
        
def any_ent_exists_in_ymap(ymap) -> bool:
    """Checks if any entity exists in the YMAP"""
    return ymap.AllEntities is not None

def get_all_ents_from_ymap(ymap) -> list:
    """Returns all the entities from the YMAP"""
    return ymap.AllEntities

def get_ent_type(entity) -> str:
    """Returns the entity type"""
    return "ENTITY" if entity.MloInstance is None else "MLOINSTANCE"

def get_ent_lod_level(entity) -> str:
    """Returns the LOD level of the entity"""
    return str(entity._CEntityDef.lodLevel)

def is_mlo_instance(entity) -> bool:
    """Returns if the entity is a MLO instance"""
    return entity.IsMlo

def get_ymap_from_file(ymap_path: str):
    """Returns the YMAP object from the file"""
    ymap_file = d.YmapFile()
    ymap_file.Load(d.File.ReadAllBytes(ymap_path))
    return ymap_file