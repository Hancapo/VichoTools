from pathlib import Path
from bpy.types import Object, Collection, Scene, Mesh, Material
from mathutils import Vector, Matrix
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from CodeWalker.GameFiles import (YmapFile) # type: ignore

from .ymap_core import (
get_ymap_from_file, 
any_ent_in_ymap, 
get_all_ents_from_ymap, 
get_all_box_occls_from_ymap, 
get_name, 
get_parent, 
get_flags, 
get_content_flags,
get_ents_extents_max,
get_ents_extents_min,
get_streaming_extents_max,
get_streaming_extents_min,
get_ymap_phys_dicts,
any_occl_exists_in_ymap,
get_all_occls_models_from_ymap,
get_ent_lod_level,
is_mlo_instance,
fill_default_entity_sets,
get_z_axis_ent,
get_ent_type,
get_ent_priority_level
)
from ..shared.helper import (
    world_corners_of,
    create_empty_obj,
    instance_obj_and_child,
    get_obj_from_scene,
    run_ops_without_view_layer_update,
    find_imported_soll_root,
    delete_hierarchy,
    delete_mesh,
    set_mask,
    get_mask,
    create_mesh_from_data,
    create_obj,
    assign_mat,
    get_mat,
)
import bpy
from ..shared.constants import (
    ENTITY_FLAGS_VALUES,
    MAP_DATA_FLAGS_VALUES,
    MAP_DATA_CONTENT_FLAGS_VALUES,
    YMAP_ASSET_EXTS,
    VALID_NON_POLY_BOUND_TYPES,
    MAPENTITY_FLAGS
)
from ..shared.funcs import get_fn_wt_ext, set_bit, indices_to_faces, sharpdx_vec_to_tuple, sharpdx_quat_to_blender_quat
from mathutils import Quaternion

_is_updating_entity_prop: bool = False
YMAP_FLAGS_UPDATING: bool = False
YMAP_CONTENT_FLAGS_UPDATING: bool = False

def create_ymap_empty(name: str, collection: Collection = None):
    """Create an empty object for a YMAP."""
    ymap_obj = create_empty_obj(name, collection)
    ymap_obj.vicho_type = "vicho_ymap_base"
    return ymap_obj

def create_ymap_entities_group(parent_ymap_obj: Object):
    """Create a group for YMAP entities."""
    ymap_entities_group = create_empty_obj(f"{parent_ymap_obj.name}.entities")
    ymap_entities_group.vicho_type = "vicho_ymap_entities"
    ymap_entities_group.parent = parent_ymap_obj
    return ymap_entities_group

def create_ymap_occluders_group(parent_ymap_obj: Object):
    """Create a group for YMAP occluders."""
    ymap_occluders_group = create_empty_obj(f"{parent_ymap_obj.name}.occluders")
    ymap_occluders_group.vicho_type = "vicho_ymap_occluder_base"
    ymap_occluders_group.parent = parent_ymap_obj
    return ymap_occluders_group

def create_ymap_box_occluders_group(parent_occl_obj: Object):
    """Create a group for YMAP box occluders."""
    ymap_box_occluders_group = create_empty_obj(f"{parent_occl_obj.name}.boxes")
    ymap_box_occluders_group.vicho_type = "vicho_ymap_box_occluders"
    ymap_box_occluders_group.parent = parent_occl_obj
    return ymap_box_occluders_group

def create_ymap_models_occluders_group(parent_occl_obj: Object):
    """Create a group for YMAP models occluders."""
    ymap_models_occluders_group = create_empty_obj(f"{parent_occl_obj.name}.models")
    ymap_models_occluders_group.vicho_type = "vicho_ymap_model_occluders"
    ymap_models_occluders_group.parent = parent_occl_obj
    return ymap_models_occluders_group

def calc_ymap_extents(entities) -> tuple[Vector, Vector, Vector, Vector]:
    """Calculates entities' and streaming extents for a YMAP."""
    inf, ninf = float("inf"), float("-inf")
    emin = Vector((inf, inf, inf))
    emax = Vector((ninf, ninf, ninf))
    smin = Vector((inf, inf, inf))
    smax = Vector((ninf, ninf, ninf))

    for ent in entities:
        obj = ent.linked_object
        if obj is None:
            continue

        corners_world = []
        corners_world.extend(world_corners_of(obj))
        for ch in obj.children_recursive:
            corners_world.extend(world_corners_of(ch))

        if not corners_world:
            continue

        bbmin_w = Vector((min(v[i] for v in corners_world) for i in range(3)))
        bbmax_w = Vector((max(v[i] for v in corners_world) for i in range(3)))

        emin = Vector((min(emin[i], bbmin_w[i]) for i in range(3)))
        emax = Vector((max(emax[i], bbmax_w[i]) for i in range(3)))

        lod_dist = ent.lod_distance if ent.lod_distance else 0.0
        sbmin_w = bbmin_w - Vector((lod_dist,) * 3)
        sbmax_w = bbmax_w + Vector((lod_dist,) * 3)
        smin = Vector((min(smin[i], sbmin_w[i]) for i in range(3)))
        smax = Vector((max(smax[i], sbmax_w[i]) for i in range(3)))

    return emin, emax, smin, smax


def deselect_all_entities_in_ymap(context, entity_scene_index=0) -> None:
    """Deselects all entities in the current YMAP"""
    from .ymap_mixin import YmapMixin
    ymap = YmapMixin.get_ymap(context)

    ymap["selected_entity_index"] = []

    for ent in ymap.entities:
        ent.is_multi_selected = False

    ymap.entity_multi_select = False

    context.scene.entity_list_index = entity_scene_index


def update_ymap_entity_prop_value(self, context, prop_name: str) -> None:
    """Update YMAP entity property value for multi-selection."""
    from .ymap_mixin import YmapMixin
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
                # print(f"Updating LOD distance to {self.lod_distance}")
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


def change_ymap_ent_parenting(objs: list[Object], do_parent=False) -> None:
    """Changes the parenting of the selected objects to the YMAP entities group"""
    scene = bpy.context.scene
    ymap_obj = scene.ymap_list[scene.ymap_list_index].ymap_object
    ymap_ent_group_obj = next(
        (obj for obj in ymap_obj.children if obj.vicho_type == "vicho_ymap_entities"),
        None,
    )
    bpy.ops.object.select_all(action="DESELECT")
    if ymap_ent_group_obj:
        for obj in objs:
            obj.select_set(True)
            if do_parent:
                obj.parent = ymap_ent_group_obj
            else:
                obj.parent = None


def update_ymap_ent_linked_obj(self, context) -> None:
    """Updates the linked object for the entity"""
    from .ymap_mixin import YmapMixin
    if not self.linked_object:
        return
    if not self.linked_object.parent:
        self.linked_object.parent = YmapMixin.get_ymap_ent_group_obj(context)
        if self.linked_object.sollum_type == "sollumz_bound_composite":
            entity = YmapMixin.get_ent(context)
            entity.sollum_type = "sollumz_bound_composite"
            entity.is_mlo_instance = True


def get_entity_sets_from_entity(context) -> list[str]:
    from .ymap_mixin import YmapMixin
    """Returns the entity sets from the entity's MLO archetype definition"""
    entity = YmapMixin.get_ent(context)
    linked_obj: Object = entity.linked_object

    for ytyp in context.scene.ytyps:
        for arch in ytyp.archetypes:
            if arch.type == "sollumz_archetype_mlo" and arch.name == linked_obj.name:
                return [es.name for es in arch.entity_sets]
    return []


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
    # update_entity_prop_value(self, context, prop_name)


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


def ymap_exist_in_scene(scene: Scene, new_ymap: str) -> bool:
    """Checks if a YMAP already exists in the scene"""
    fn: str = get_fn_wt_ext(new_ymap)
    ymap_list = scene.ymap_list
    if len(ymap_list) > 0:
        for ymap in ymap_list:
            if ymap.name == fn:
                return True
    return False


def import_ymap_to_scene(
    scene: Scene, new_ymap_path: str, import_settings, self, asset_path: str
) -> bool:
    p: Path = Path(new_ymap_path)
    filename: str = p.stem
    if not ymap_exist_in_scene(scene, new_ymap_path):
        new_ymap = scene.ymap_list.add()
        scene.ymap_list_index = len(scene.ymap_list) - 1
        new_ymap.active_category = "DATA"
        bpy.ops.ymap.map_data_menu(operator_id="ymap.map_data_menu")
        current_index: int = len(scene.ymap_list) - 1
        ymap_file: "YmapFile" = get_ymap_from_file(new_ymap_path)
        fill_map_data_from_ymap(
            scene, current_index, ymap_file, import_settings.import_props
        )
        ymap_obj: Object = create_ymap_empty(filename)
        new_ymap.ymap_object = ymap_obj
        if import_settings.import_entities and asset_path is not None:
            ymap_ent_group: Object = create_ymap_entities_group(ymap_obj)
            new_ymap.ymap_entity_group_object = ymap_ent_group
            import_ent_objs(
                import_settings, scene, current_index, asset_path, ymap_ent_group, self
            )
        if import_settings.import_occluders:
            import_occl_objs(
                scene, current_index, ymap_file, ymap_obj, self)
        self.report({"INFO"}, f"YMAP {filename} added to scene")
        return True
    else:
        self.report({"ERROR"}, f"YMAP {filename} already exists in scene")
        return False


def remove_ymap_from_scene(scene: Scene, index: int, delete_all: bool) -> bool:
    """Removes a YMAP from the scene"""
    ymap_obj: Object = scene.ymap_list[index].ymap_object
    ymap_ent_grp: Object = scene.ymap_list[index].ymap_entity_group_object
    if delete_all:
        delete_hierarchy(ymap_obj)
        return True

    if ymap_ent_grp:
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


def fill_map_data_from_ymap(
    scene: Scene, index: int, current_ymap, do_props: bool
) -> None:
    """Fills the data from the imported YMAP"""
    any_entities = any_ent_in_ymap(current_ymap)
    scene.ymap_list[index].name = get_name(current_ymap)
    scene.ymap_list[index].parent = get_parent(current_ymap)
    scene.ymap_list[index].flags.total_flags = get_flags(current_ymap)
    scene.ymap_list[index].content_flags.total_flags = get_content_flags(current_ymap)
    scene.ymap_list[index].streaming_extents_min = get_streaming_extents_min(
        current_ymap
    )
    scene.ymap_list[index].streaming_extents_max = get_streaming_extents_max(
        current_ymap
    )
    scene.ymap_list[index].entities_extents_min = get_ents_extents_min(current_ymap)
    scene.ymap_list[index].entities_extents_max = get_ents_extents_max(current_ymap)
    scene.ymap_list[index].any_entities = any_entities
    scene.ymap_list[index].is_imported = True

    fill_physics_dicts_from_ymap(scene, index, current_ymap)
    fill_ents_data_from_ymap(scene, index, current_ymap, any_entities, do_props)


def fill_ents_data_from_ymap(
    scene: Scene, index: int, current_ymap, any_ents: bool, do_props: bool
) -> None:
    """Fills the entity data from the imported YMAP"""
    if any_ents:
        for ent in get_all_ents_from_ymap(current_ymap):
            if (
                not do_props
                and get_ent_lod_level(ent) == "LODTYPES_DEPTH_ORPHANHD"
                and not is_mlo_instance(ent)
            ):
                continue
            new_entity = scene.ymap_list[index].entities.add()
            if is_mlo_instance(ent):
                new_entity.is_mlo_instance = True
                new_entity.group_id = ent.MloInstance.Instance.groupId
                new_entity.floor_id = ent.MloInstance.Instance.floorId
                new_entity.mlo_inst_flags = ent.MloInstance.Instance.MLOInstflags
                new_entity.num_exit_portals = ent.MloInstance.Instance.numExitPortals
                fill_default_entity_sets(ent, new_entity)
            new_entity.archetype_name = ent.CEntityDef.archetypeName.ToString()
            new_entity.flags.total_flags = ent.CEntityDef.flags
            new_entity.guid = str(ent.CEntityDef.guid)
            new_entity.position = (
                ent.CEntityDef.position.X,
                ent.CEntityDef.position.Y,
                ent.CEntityDef.position.Z,
            )
            new_entity.rotation = (
                -ent.CEntityDef.rotation.W,
                ent.CEntityDef.rotation.X,
                ent.CEntityDef.rotation.Y,
                get_z_axis_ent(ent),
            )
            new_entity.scale_xy = ent.CEntityDef.scaleXY
            new_entity.scale_z = ent.CEntityDef.scaleZ
            new_entity.parent_index = ent.CEntityDef.parentIndex
            new_entity.lod_distance = ent.CEntityDef.lodDist
            new_entity.child_lod_distance = ent.CEntityDef.childLodDist
            new_entity.num_children = ent.CEntityDef.numChildren
            new_entity.lod_level = get_ent_lod_level(ent)
            new_entity.priority_level = get_ent_priority_level(ent)
            new_entity.ambient_occlusion_multiplier = (
                ent.CEntityDef.ambientOcclusionMultiplier
            )
            new_entity.artificial_ambient_occlusion = (
                ent.CEntityDef.artificialAmbientOcclusion
            )
            new_entity.tintValue = ent.CEntityDef.tintValue
            new_entity.type = get_ent_type(ent)
            new_entity.ent_index = (
                0
                if len(scene.ymap_list[index].entities) == -1
                else len(scene.ymap_list[index].entities) - 1
            )


def import_ent_objs(
    import_settings, scene: Scene, index: int, asset_path: str, ymap_group: Object, self
) -> None:
    entities: list = scene.ymap_list[index].entities
    for e in entities:
        p: Path = Path(asset_path)
        print(f"Is MLO: {e.is_mlo_instance}")
        file_found: bool = False
        bin_file: str = None
        for ext in YMAP_ASSET_EXTS:
            if Path.exists(p / f"{e.archetype_name}.{ext}"):
                bin_file: str = f"{e.archetype_name}.{ext}"
                file_found = True
                break
        if not file_found:
            self.report(
                {"ERROR"}, f"Could not find the binary file for {e.archetype_name}"
            )
            continue

        before_import: set[str] = set(bpy.data.objects.keys())
        if Path.exists(p / bin_file):
            working_obj: Object = None
            if not get_obj_from_scene(scene, e.archetype_name):

                def fast_import():
                    print(f"Trying to import {bin_file}")
                    bpy.ops.sollumz.import_assets(
                        directory=str(p), files=[{"name": bin_file}]
                    )

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
            purify_asset(
                import_settings.remove_cols,
                import_settings.remove_lights,
                import_settings.remove_non_high,
                working_obj,
            )

def import_occl_objs(scene: Scene, index: int, ymap_file, ymap_obj: Object, self) -> None:

    if any_occl_exists_in_ymap(ymap_file):
        ymap_occl_group: Object = create_ymap_occluders_group(ymap_obj)

        box_occls = get_all_box_occls_from_ymap(ymap_file)
        model_occls = get_all_occls_models_from_ymap(ymap_file)

        if box_occls:
            box_occls_group: Object = create_ymap_box_occluders_group(ymap_occl_group)
            for box_occl in box_occls:
                fill_box_occl_data_from_ymap(scene, index, box_occls_group, box_occl)

        if model_occls:
            model_occls_group: Object = create_ymap_models_occluders_group(ymap_occl_group)
            for model_occl in model_occls:
                fill_model_occl_data_from_ymap(scene, index, model_occls_group, model_occl)

def fill_model_occl_data_from_ymap(scene: Scene, index: int, group_obj: Object, model_occl) -> None:
    new_model_occl = scene.ymap_list[index].ymap_model_occluders.add()
    new_model_occl.name = f"Occluder Model {model_occl.Index}"
    new_model_occl.flags = model_occl.Flags.Value
    new_obj: Object = create_model_occluder_obj(model_occl.Index, model_occl)
    new_obj.parent = group_obj
    new_model_occl.linked_obj = new_obj

def fill_box_occl_data_from_ymap(scene: Scene, index: int, group_obj: Object, box_occl) -> None:
    new_box_occl = scene.ymap_list[index].ymap_box_occluders.add()
    new_box_occl.name = f"Box Occluder {box_occl.Index}"
    new_obj: Object = create_box_occluder_obj(box_occl.Index, box_occl)
    new_obj.parent = group_obj
    new_box_occl.linked_obj = new_obj

def create_model_occluder_obj(index, model_occl) -> Object:
    faces: list[tuple] = indices_to_faces(model_occl.Indices)
    verts: list[tuple[float, float, float]] = [sharpdx_vec_to_tuple(v) for v in model_occl.Vertices]
    mesh: Mesh = create_mesh_from_data(f"ModelOccl{index}", verts, faces)
    new_obj: Object = create_obj(f"ModelOccl{index}", True, mesh)
    assign_mat(new_obj, get_mat("ModelOccluderMat", (1, 0.5, 0, 1), 0.895, 1))
    return new_obj

def create_box_occluder_obj(index: int, box_occl) -> Object:
    xmin, ymin, zmin = sharpdx_vec_to_tuple(box_occl.BBMin)
    xmax, ymax, zmax = sharpdx_vec_to_tuple(box_occl.BBMax)
    position: Vector = sharpdx_vec_to_tuple(box_occl.Position)
    rotation: Quaternion = sharpdx_quat_to_blender_quat(box_occl.Orientation)

    verts: list[tuple[float, float, float]] = [
        (xmin, ymin, zmin),
        (xmax, ymin, zmin),
        (xmax, ymax, zmin),
        (xmin, ymax, zmin),
        (xmin, ymin, zmax),
        (xmax, ymin, zmax),
        (xmax, ymax, zmax),
        (xmin, ymax, zmax)
    ]

    faces = [
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]

    mesh: Mesh = create_mesh_from_data(f"BoxOccl{index}", verts, faces)
    new_obj: Object = create_obj(f"BoxOccl{index}", True, mesh)
    new_obj.location = position
    new_obj.rotation_mode = "QUATERNION"
    new_obj.rotation_quaternion = rotation
    assign_mat(new_obj, get_mat("BoxOccluderMat", (0, 1, 0, 1), 0.5, 1))
    return new_obj

    

def get_imported_asset(before_import, entity) -> None:
    after_import: set[str] = set(bpy.data.objects.keys())
    new_objs_names: set[str] = after_import - before_import
    new_objs: list[object] = [bpy.data.objects[name] for name in new_objs_names]
    imported_obj: Object = find_imported_soll_root(entity.archetype_name, new_objs)
    return imported_obj


def purify_asset(
    del_cols: bool, del_lights: bool, del_non_high: bool, obj: Object
) -> None:
    print(f"Purifying asset: {obj.name}")
    if del_cols:
        delete_all_cols(obj)
    if del_lights:
        delete_all_lights(obj)
    if del_non_high:
        draw_models: list[Object] = [
            child
            for child in obj.children_recursive
            if child.sollum_type == "sollumz_drawable_model"
        ]
        if draw_models:
            for draw_model in draw_models:
                remove_non_high_meshes(draw_model)


def delete_all_cols(obj: Object) -> None:
    """Deletes all collision objects from the given object"""
    bound_compo: list[Object] = [
        child
        for child in obj.children
        if child.sollum_type == "sollumz_bound_composite"
    ]
    if bound_compo:
        for compo in bound_compo:
            delete_hierarchy(compo)
    cols_to_delete: list[Object] = [
        child
        for child in obj.children
        if child.sollum_type in VALID_NON_POLY_BOUND_TYPES
    ]
    if cols_to_delete:
        for col in cols_to_delete:
            delete_hierarchy(col)


def delete_all_lights(obj: Object) -> None:
    lights_group: Object = next(
        (
            child
            for child in obj.children
            if ".lights" in child.name or "Lights" in child.name
        ),
        None,
    )
    delete_hierarchy(lights_group) if lights_group else None


def remove_non_high_meshes(obj: Object) -> None:
    delete_mesh(obj.sz_lods.very_low.mesh) if obj.sz_lods.very_low.mesh else None
    obj.sz_lods.very_low.mesh_name = ""
    delete_mesh(obj.sz_lods.low.mesh) if obj.sz_lods.low.mesh else None
    obj.sz_lods.low.mesh_name = ""
    delete_mesh(obj.sz_lods.medium.mesh) if obj.sz_lods.medium.mesh else None
    obj.sz_lods.medium.mesh_name = ""
    delete_mesh(obj.sz_lods.very_high.mesh) if obj.sz_lods.very_high.mesh else None
    obj.sz_lods.very_high.mesh_name = ""


def apply_transforms_to_obj_from_entity(obj: Object, entity) -> None:
    """Applies the transforms from the entity to the object"""
    if obj is not None:
        entity.linked_object = obj
        entity.linked_object.location = entity.position
        entity.linked_object.rotation_mode = "QUATERNION"
        entity.linked_object.rotation_quaternion = entity.rotation
        entity.linked_object.scale = (entity.scale_xy, entity.scale_xy, entity.scale_z)


# This function is almost a copy of the CodeWalker's one.
def calc_ymap_flags(bl_ymap) -> tuple[int, int]:
    """Calculates all flags for the YMAP"""
    flags: int = 0
    content_flags: int = 0

    if bl_ymap.entities:
        for ent in bl_ymap.entities:
            match ent.lod_level:
                case "LODTYPES_DEPTH_HD" | "LODTYPES_DEPTH_ORPHANHD":
                    content_flags = set_bit(content_flags, 0)
                case "LODTYPES_DEPTH_LOD":
                    content_flags = set_bit(content_flags, 1)
                case "LODTYPES_DEPTH_SLOD1":
                    content_flags = set_bit(content_flags, 4)
                    flags = set_bit(flags, 1)
                case (
                    "LODTYPES_DEPTH_SLOD2"
                    | "LODTYPES_DEPTH_SLOD3"
                    | "LODTYPES_DEPTH_SLOD4"
                ):
                    content_flags = set_bit(content_flags, 2)
                    content_flags = set_bit(content_flags, 4)
                    flags = set_bit(flags, 1)
                case _:
                    pass
            if ent.is_mlo_instance:
                content_flags = set_bit(content_flags, 3)

    if bl_ymap.ymap_phys_dicts:
        content_flags = set_bit(content_flags, 6)

    if bl_ymap.ymap_box_occluders or bl_ymap.ymap_model_occluders:
        content_flags = set_bit(content_flags, 5)


    return flags, content_flags


def set_ymap_ent_extents(ymap, entities):
    """Sets the entity extents of the YMAP based on the given entities."""
    ent_min, ent_max, _, _ = calc_ymap_extents(entities)
    ymap.entities_extents_min = ent_min
    ymap.entities_extents_max = ent_max


def set_ymap_strm_extents(ymap, entities):
    """Sets the streaming extents of the YMAP based on the given entities."""
    _, _, strm_min, strm_max = calc_ymap_extents(entities)
    ymap.streaming_extents_min = strm_min
    ymap.streaming_extents_max = strm_max



def get_total_flags(self):
    return get_mask(self, "flags")

def set_total_flags(self, value):
    set_mask(self, "flags", value, MAPENTITY_FLAGS)


def box_occluder_mat() -> Material:
    return get_mat("BoxOccluderMat", (0, 1, 0, 1), 0.5, 1)

def occluder_model_mat() -> Material:
    return get_mat("ModelOccluderMat", (1, 0.5, 0, 1), 0.895, 1)

def create_box_occluder_item(box_obj: Object, ymap, ymap_box_occl_group) -> None:
    """Creates a box occlusion culling object in the YMAP"""
    box_obj.name = "Box Occluder"
    new_box_occl = ymap.ymap_box_occluders.add()
    new_box_occl.name = "Box Occluder"
    new_box_occl.linked_obj = box_obj
    box_obj.parent = ymap_box_occl_group
    assign_mat(box_obj, box_occluder_mat())

def create_occluder_model_item(model_obj: Object, ymap, ymap_occl_model_group) -> None:
    """Creates an occlusion culling model object in the YMAP"""
    model_obj.name = "Occluder Model"
    new_occl_model = ymap.ymap_model_occluders.add()
    new_occl_model.name = "Occluder Model"
    new_occl_model.linked_obj = model_obj
    set_parent_keep_world(model_obj, ymap_occl_model_group)
    assign_mat(model_obj, occluder_model_mat())

def set_parent_keep_world(child: Object, new_parent: Object | None) -> None:
    """Sets the parent of an object while keeping its world position and rotation."""
    mw: Matrix = child.matrix_world.copy()

    child.parent = new_parent
    child.parent_type = "OBJECT"

    if new_parent is None:
        child.matrix_parent_inverse = Matrix.Identity(4)
    else:
        child.matrix_parent_inverse = new_parent.matrix_world.inverted() @ mw

    child.matrix_world = mw

