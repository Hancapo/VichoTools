from ..vicho_dependencies import dependencies_manager as d
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from CodeWalker.GameFiles import (YmapFile,  # type: ignore
                                      MetaHash,
                                      YmapEntityDef,
                                      YmapBoxOccluder,
                                      YmapOccludeModel)

def get_name(ymap: "YmapFile") -> str:
    """Returns the name of the YMAP"""
    return ymap.CMapData.name.ToString()


def get_parent(ymap: "YmapFile") -> str:
    """Returns the parent of the YMAP"""
    return ymap.CMapData.parent.ToString()


def get_flags(ymap: "YmapFile") -> int:
    """Returns the flags of the YMAP"""
    return ymap.CMapData.flags


def get_content_flags(ymap: "YmapFile") -> int:
    """Returns the content flags of the YMAP"""
    return ymap.CMapData.contentFlags


def get_streaming_extents_min(ymap: "YmapFile") -> tuple[float, float, float]:
    """Returns the streaming extents min of the YMAP"""
    return (
        ymap.CMapData.streamingExtentsMin.X,
        ymap.CMapData.streamingExtentsMin.Y,
        ymap.CMapData.streamingExtentsMin.Z,
    )


def get_streaming_extents_max(ymap: "YmapFile") -> tuple[float, float, float]:
    """Returns the streaming extents max of the YMAP"""
    return (
        ymap.CMapData.streamingExtentsMax.X,
        ymap.CMapData.streamingExtentsMax.Y,
        ymap.CMapData.streamingExtentsMax.Z,
    )


def get_ents_extents_min(ymap: "YmapFile") -> tuple[float, float, float]:
    """Returns the entities extents min of the YMAP"""
    return (
        ymap.CMapData.entitiesExtentsMin.X,
        ymap.CMapData.entitiesExtentsMin.Y,
        ymap.CMapData.entitiesExtentsMin.Z,
    )


def get_ents_extents_max(ymap: "YmapFile") -> tuple[float, float, float]:
    """Returns the entities extents max of the YMAP"""
    return (
        ymap.CMapData.entitiesExtentsMax.X,
        ymap.CMapData.entitiesExtentsMax.Y,
        ymap.CMapData.entitiesExtentsMax.Z,
    )


def get_ymap_phys_dicts(ymap: "YmapFile") -> list:
    """Returns the physics dictionaries of the YMAP"""
    phys_dicts: list["MetaHash"] = []
    for phys_dict in ymap.physicsDictionaries:
        phys_dicts.append(phys_dict.ToString())
    return phys_dicts

def any_ent_in_ymap(ymap: "YmapFile") -> bool:
    """Checks if any entity exists in the YMAP"""
    return get_all_ents_from_ymap(ymap) is not None


def get_all_ents_from_ymap(ymap: "YmapFile") -> list["YmapEntityDef"]:
    """Returns all the entities from the YMAP"""
    return ymap.AllEntities

def get_all_occls_models_from_ymap(ymap: "YmapFile") -> list["YmapOccludeModel"]:
    """Returns all the occluder models from the YMAP"""
    return ymap.OccludeModels

def get_all_box_occls_from_ymap(ymap: "YmapFile") -> list["YmapBoxOccluder"]:
    """Returns all the box occluders from the YMAP"""
    return ymap.BoxOccluders


def any_occl_exists_in_ymap(ymap) -> bool:
    """Checks if any occluder exists in the YMAP"""
    return (
        any_box_occl_exists_in_ymap(ymap) or any_model_occl_exists_in_ymap(ymap)
    )

def any_box_occl_exists_in_ymap(ymap) -> bool:
    """Checks if any box occluder exists in the YMAP"""
    return get_all_box_occls_from_ymap(ymap) is not None

def any_model_occl_exists_in_ymap(ymap) -> bool:
    """Checks if any model occluder exists in the YMAP"""
    return get_all_occls_models_from_ymap(ymap) is not None

def get_ent_type(entity: "YmapEntityDef") -> str:
    """Returns the entity type"""
    return "ENTITY" if entity.MloInstance is None else "MLOINSTANCE"


def get_ent_lod_level(entity: "YmapEntityDef") -> str:
    """Returns the LOD level of the entity"""
    return str(entity.CEntityDef.lodLevel)


def get_ent_priority_level(entity: "YmapEntityDef") -> str:
    """Returns the priority level of the entity"""
    return str(entity.CEntityDef.priorityLevel)


def fill_default_entity_sets(entity: "YmapEntityDef", bld_entity) -> None:
    """Returns the default entity sets of the MLO instance"""
    if entity.MloInstance:
        if entity.MloInstance.defaultEntitySets is None:
            return
        sets: list[str] = [ent_set.ToString() for ent_set in entity.MloInstance.defaultEntitySets]

    if sets:
        for ent_set in sets:
            new = bld_entity.default_entity_sets.add()
            new.name = ent_set


def build_default_entity_sets_list(dels: list[str]) -> None:
    """Builds the list for the default entity sets property"""
    return None


def is_mlo_instance(entity: "YmapEntityDef") -> bool:
    """Returns if the entity is a MLO instance"""
    return entity.IsMlo


def get_ymap_from_file(ymap_path: str):
    """Returns the YMAP object from the file"""
    ymap_file: "YmapFile" = d.YmapFile()
    ymap_file.Load(d.File.ReadAllBytes(ymap_path))
    return ymap_file


def get_z_axis_ent(ent: "YmapEntityDef"):
    """Returns the Z axis of the entity as negative if it is not a MLO instance otherwise positive"""
    return (
        ent.CEntityDef.rotation.Z
        if not is_mlo_instance(ent)
        else -ent.CEntityDef.rotation.Z
    )