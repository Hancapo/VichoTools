from .properties import EntityProps
from ..vicho_dependencies import dependencies_manager as d
from pathlib import Path
from .helper import run_ops_without_view_layer_update, instance_obj_and_child, get_obj_from_scene, get_fn_wt_ext
import bpy
from .constants import COMPAT_SOLL_TYPES, OBJECT_TYPES, VALID_NON_POLY_BOUND_TYPES, SOLLUMZ_EXTS
from bpy.types import Object, Scene
from ..misc.funcs import create_ymap_empty, create_ymap_entities_group, delete_hierarchy, delete_mesh
from mathutils import Vector


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

def get_ymap_phys_dicts(ymap) -> list:
    """Returns the physics dictionaries of the YMAP"""
    phys_dicts = []
    for phys_dict in ymap.physicsDictionaries:
        phys_dicts.append(phys_dict.ToString())
    return phys_dicts

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
        new_ymap = scene.ymap_list.add()
        scene.ymap_list_index = len(scene.ymap_list) - 1
        new_ymap.active_category = "DATA"
        bpy.ops.ymap.map_data_menu(operator_id="ymap.map_data_menu")
        current_index = len(scene.ymap_list) - 1
        ymap_file = get_ymap_from_file(new_ymap_path)
        fill_map_data_from_ymap(scene, current_index, ymap_file, do_props)
        ymap_obj: Object = create_ymap_empty(filename)
        new_ymap.ymap_object = ymap_obj
        if i_ents and assets_path is not None:
            ymap_ent_group: Object = create_ymap_entities_group(ymap_obj)
            new_ymap.ymap_entity_group_object = ymap_ent_group
            import_ent_objs(scene, current_index, assets_path, ymap_ent_group, self)
        self.report({'INFO'}, f"YMAP {filename} added to scene")
        return True
    else:
        self.report({'ERROR'}, f"YMAP {filename} already exists in scene")
        return False
 
def remove_ymap_from_scene(scene: Scene, index: int, delete_all: bool) -> bool:
    """Removes a YMAP from the scene"""
    ymap_obj: Object = scene.ymap_list[index].ymap_object
    ymap_ent_grp: Object = scene.ymap_list[index].ymap_entity_group_object
    if delete_all:
        delete_hierarchy(ymap_obj)
        return True

    if ymap_ent_grp.children: 
        for ent in ymap_ent_grp.children:
            ent.parent = None
            ent.vicho_ymap_parent = None

    delete_hierarchy(ymap_obj)
    
    return True

def add_ymap_to_scene(scene: Scene) -> None:
    """Adds a YMAP to the scene"""
    scene.ymap_list.add()
    scene.ymap_list_index = len(scene.ymap_list) + 1
    
def fill_physics_dicts_from_ymap(scene: Scene, index: int, current_ymap) -> None:
    """Fills the physics dictionaries from the selected YMAP"""
    if current_ymap.physicsDictionaries is not None:
        for phys_dict in get_ymap_phys_dicts(current_ymap):
            new_phys_dict = scene.ymap_list[index].ymap_phys_dicts.add()
            new_phys_dict.name = phys_dict

def fill_map_data_from_ymap(scene: Scene, index: int, current_ymap, do_props: bool) -> None:
    """Fills the data from the imported YMAP"""
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
    
    fill_physics_dicts_from_ymap(scene, index, current_ymap)
    fill_ents_data_from_ymap(scene, index, current_ymap, any_entities, do_props)
        

def fill_ents_data_from_ymap(scene: Scene, index: int, current_ymap, any_ents: bool, do_props: bool) -> None:
    """Fills the entity data from the imported YMAP"""
    if any_ents:
        for ent in get_all_ents_from_ymap(current_ymap):
            if not do_props and get_ent_lod_level(ent) == "LODTYPES_DEPTH_ORPHANHD" and not is_mlo_instance(ent):
                continue
            new_entity = scene.ymap_list[index].entities.add()
            if is_mlo_instance(ent):
                new_entity.is_mlo_instance = True
                new_entity.group_id = ent.MloInstance.Instance.groupId
                new_entity.floor_id = ent.MloInstance.Instance.floorId
                new_entity.mlo_inst_flags = ent.MloInstance.Instance.MLOInstflags
                new_entity.num_exit_portals = ent.MloInstance.Instance.numExitPortals
                fill_default_entity_sets(ent, new_entity)
            new_entity.archetype_name = ent._CEntityDef.archetypeName.ToString()
            new_entity.flags.total_flags = ent._CEntityDef.flags
            new_entity.guid = str(ent._CEntityDef.guid)
            new_entity.position = (ent._CEntityDef.position.X, ent._CEntityDef.position.Y, ent._CEntityDef.position.Z)
            new_entity.rotation = (-ent._CEntityDef.rotation.W, ent._CEntityDef.rotation.X, ent._CEntityDef.rotation.Y, get_z_axis_ent(ent))
            new_entity.scale_xy = ent._CEntityDef.scaleXY
            new_entity.scale_z = ent._CEntityDef.scaleZ
            new_entity.parent_index = ent._CEntityDef.parentIndex
            new_entity.lod_distance = ent._CEntityDef.lodDist
            new_entity.child_lod_distance = ent._CEntityDef.childLodDist
            new_entity.num_children = ent._CEntityDef.numChildren
            new_entity.lod_level = get_ent_lod_level(ent)
            new_entity.priority_level = get_ent_priority_level(ent)
            new_entity.ambient_occlusion_multiplier = ent._CEntityDef.ambientOcclusionMultiplier
            new_entity.artificial_ambient_occlusion = ent._CEntityDef.artificialAmbientOcclusion
            new_entity.tintValue = ent._CEntityDef.tintValue
            new_entity.type = get_ent_type(ent)
    

def import_ent_objs(scene: Scene, index: int, asset_path: str, ymap_group: Object, self) -> None:
    entities: list[EntityProps] = scene.ymap_list[index].entities
    for e in entities:
        p: Path = Path(asset_path)
        print(f"Is MLO: {e.is_mlo_instance}")
        file_found: bool = False
        xml_file: str = None
        for ext in SOLLUMZ_EXTS:
            if Path.exists(p / f"{e.archetype_name}.{ext}.xml"):
                xml_file: str = f"{e.archetype_name}.{ext}.xml"
                file_found = True
                break
        if not file_found:
            self.report({'ERROR'}, f"Could not find the XML file for {e.archetype_name}")
            continue
        
        before_import: set[str] = set(bpy.data.objects.keys())
        if Path.exists(p / xml_file):
            working_obj: Object = None
            if not get_obj_from_scene(scene, e.archetype_name):
                def fast_import():
                    print(f"Trying to import {xml_file}")
                    bpy.ops.sollumz.import_assets(directory=str(p), files=[{"name": xml_file}])
                run_ops_without_view_layer_update(fast_import)
                working_obj: Object = get_imported_asset(before_import, e)
                print(f"Working obj: {working_obj}")
            else:
                existing_obj = get_obj_from_scene(scene, e.archetype_name)
                if existing_obj is not None:
                    working_obj: Object = instance_obj_and_child(existing_obj)
            apply_transforms_to_obj_from_entity(working_obj, e)
            working_obj.parent = ymap_group
            working_obj.vicho_ymap_parent = ymap_group.parent
            purify_asset(working_obj)

def get_obj_soll_parent(filename: str, new_objs: list[Object]) -> Object:
    return next((x for x in new_objs if filename in x.name and
                 x.type in OBJECT_TYPES and
                 x.sollum_type in COMPAT_SOLL_TYPES and
                 not x.parent), None)

def get_imported_asset(before_import, entity) -> None:
    after_import: set[str] = set(bpy.data.objects.keys())
    new_objs_names: set[str] = after_import - before_import
    new_objs: list[object] = [bpy.data.objects[name] for name in new_objs_names]
    imported_obj: Object = get_obj_soll_parent(entity.archetype_name, new_objs)
    return imported_obj

def purify_asset(obj: Object) -> None:
    print(f"Purifying asset: {obj.name}")
    delete_all_cols(obj)
    delete_all_lights(obj)
    draw_models: list[Object] = [child for child in obj.children if child.sollum_type == "sollumz_drawable_model"]
    if draw_models:
        for draw_model in draw_models:
            remove_non_high_meshes(draw_model)

def delete_all_cols(obj: Object) -> None:
    """Deletes all collision objects from the given object"""
    bound_compo: list[Object] = [child for child in obj.children if child.sollum_type == "sollumz_bound_composite"]
    if bound_compo:
        for compo in bound_compo:
            delete_hierarchy(compo)
    cols_to_delete: list[Object] = [child for child in obj.children if child.sollum_type in VALID_NON_POLY_BOUND_TYPES]
    if cols_to_delete:
        for col in cols_to_delete:
            delete_hierarchy(col)

def delete_all_lights(obj: Object) -> None:
    lights_group: Object = next((child for child in obj.children if ".lights" in child.name or "Lights" in child.name), None)
    delete_hierarchy(lights_group) if lights_group else None

def remove_non_high_meshes(obj: Object) -> None:
    delete_mesh(obj.sz_lods.very_low.mesh) if obj.sz_lods.very_low.mesh else None
    obj.sz_lods.very_low.mesh_name = ''
    delete_mesh(obj.sz_lods.low.mesh) if obj.sz_lods.low.mesh else None
    obj.sz_lods.low.mesh_name = ''
    delete_mesh(obj.sz_lods.medium.mesh) if obj.sz_lods.medium.mesh else None
    obj.sz_lods.medium.mesh_name = ''
    delete_mesh(obj.sz_lods.very_high.mesh) if obj.sz_lods.very_high.mesh else None
    obj.sz_lods.very_high.mesh_name = ''

def apply_transforms_to_obj_from_entity(obj:Object, entity: "EntityProps") -> None:
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

def get_ent_priority_level(entity) -> str:
    """Returns the priority level of the entity"""
    return str(entity._CEntityDef.priorityLevel)


def fill_default_entity_sets(entity, bld_entity) -> None:
    """Returns the default entity sets of the MLO instance"""
    if entity.MloInstance:
        sets = [ent_set.ToString() for ent_set in entity.MloInstance.defaultEntitySets]
        
    if sets:
        for ent_set in sets:
            new = bld_entity.default_entity_sets.add()
            new.name = ent_set

def build_default_entity_sets_list(dels: list[str]) -> None:
    """Builds the list for the default entity sets property"""
    return None

def is_mlo_instance(entity) -> bool:
    """Returns if the entity is a MLO instance"""
    return entity.IsMlo


def get_ymap_from_file(ymap_path: str):
    """Returns the YMAP object from the file"""
    ymap_file = d.YmapFile()
    ymap_file.Load(d.File.ReadAllBytes(ymap_path))
    return ymap_file

def get_z_axis_ent(ent):
    """Returns the Z axis of the entity as negative if it is not a MLO instance otherwise positive"""
    return ent._CEntityDef.rotation.Z if not is_mlo_instance(ent) else -ent._CEntityDef.rotation.Z

def sanitize_name(name: str) -> str:
    new_name: str = ""
    if '.' in name:
        new_name = name.split('.')[0]
    else:
        new_name = name
    return new_name

def set_bit(value: int, bit: int) -> int:
    """Sets a specific bit in an integer value"""
    return value | (1 << bit)

# This function is almost a copy of the CodeWalker's one.
def calc_ymap_flags(ymap) -> tuple[int, int]:
    """Calculates all flags for the YMAP"""
    flags = 0
    content_flags = 0
    
    if ymap.entities:
        for ent in ymap.entities:
            match ent.lod_level:
                case "LODTYPES_DEPTH_HD":
                    content_flags = set_bit(content_flags, 0)
                    break
                case "LODTYPES_DEPTH_LOD":
                    content_flags = set_bit(content_flags, 1)
                    break
                case "LODTYPES_DEPTH_SLOD1":
                    content_flags = set_bit(content_flags, 4)
                    flags = set_bit(flags, 1)
                    break
                case "LODTYPES_DEPTH_SLOD4":
                    content_flags = set_bit(content_flags, 2)
                    content_flags = set_bit(content_flags, 4)
                    flags = set_bit(flags, 1)
                    break
            if ent.is_mlo_instance:
                content_flags = set_bit(content_flags, 3)
        
    return flags, content_flags

def get_children_aabb(parent: Object):
    """Calculates the axis-aligned bounding box of all children of the given parent object."""
    inf, ninf = float('inf'), float('-inf')
    bb_min = Vector(( inf,  inf,  inf))
    bb_max = Vector((ninf, ninf, ninf))
    inv_parent = parent.matrix_world.inverted()

    for child in parent.children_recursive:
        if child.type != 'MESH' and child.sollum_type != "sollumz_drawable_model":
            continue
        for corner in child.bound_box:
            world_pt = child.matrix_world @ Vector(corner)
            local_pt = inv_parent @ world_pt
            bb_min.x = min(bb_min.x, local_pt.x)
            bb_min.y = min(bb_min.y, local_pt.y)
            bb_min.z = min(bb_min.z, local_pt.z)
            bb_max.x = max(bb_max.x, local_pt.x)
            bb_max.y = max(bb_max.y, local_pt.y)
            bb_max.z = max(bb_max.z, local_pt.z)

    return bb_min, bb_max

def set_ymap_ent_extents(ymap, entities):
    """Sets the entity extents of the YMAP based on the given entities."""
    emin, emax, _, _ = calc_extents(entities)
    ymap.entities_extents_min = emin
    ymap.entities_extents_max = emax
    
def set_ymap_strm_extents(ymap, entities):
    """Sets the streaming extents of the YMAP based on the given entities."""
    _, _, smin, smax = calc_extents(entities)
    ymap.streaming_extents_min = smin
    ymap.streaming_extents_max = smax

# I don't understand this function tbh, thanks dexy and ChatGPT, I guess. I don't have high expectations for this one anyway (it worked lmao).
def calc_extents(entities):
    """Calculates the extents of the entities in the YMAP."""
    inf, ninf = float('inf'), float('-inf')
    emin = Vector(( inf,  inf,  inf))
    emax = Vector((ninf, ninf, ninf))
    smin = Vector(( inf,  inf,  inf))
    smax = Vector((ninf, ninf, ninf))

    for ent in entities:
        obj = ent.linked_object
        mw = obj.matrix_world
        lod_dist = ent.lod_distance
        bb_min_loc, bb_max_loc = get_children_aabb(obj)
        corners = [
            Vector((x, y, z))
            for x in (bb_min_loc.x, bb_max_loc.x)
            for y in (bb_min_loc.y, bb_max_loc.y)
            for z in (bb_min_loc.z, bb_max_loc.z)
        ]
        world_c = [mw @ v for v in corners]
        bbmin_w = Vector((min(v[i] for v in world_c) for i in range(3)))
        bbmax_w = Vector((max(v[i] for v in world_c) for i in range(3)))

        emin = Vector((min(emin[i], bbmin_w[i]) for i in range(3)))
        emax = Vector((max(emax[i], bbmax_w[i]) for i in range(3)))

        inf_min = bb_min_loc - Vector((lod_dist,)*3)
        inf_max = bb_max_loc + Vector((lod_dist,)*3)
        stream_corners = [
            Vector((x, y, z))
            for x in (inf_min.x, inf_max.x)
            for y in (inf_min.y, inf_max.y)
            for z in (inf_min.z, inf_max.z)
        ]
        world_s = [mw @ v for v in stream_corners]
        sbmin_w = Vector((min(v[i] for v in world_s) for i in range(3)))
        sbmax_w = Vector((max(v[i] for v in world_s) for i in range(3)))

        smin = Vector((min(smin[i], sbmin_w[i]) for i in range(3)))
        smax = Vector((max(smax[i], sbmax_w[i]) for i in range(3)))

    return emin, emax, smin, smax

    