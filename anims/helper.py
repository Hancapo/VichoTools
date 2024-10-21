from typing import List
from .anim_object import AnimObject
from ..misc.constants import ANIM_SOLLUM_TYPES
from ..misc.funcs import is_drawable_model, is_drawable
from .target import Target
from .enums import AnimationType, GroupType, ChildType
import bpy
from bpy.types import Object, Action
from .uv_anim import UvAnim

def get_anim_objs_from_sel(objs: List[Object]) -> List[AnimObject]:
    """Create a list of AnimObjects from a list of selected objects"""

    anim_objs: List[AnimObject] = []

    if not objs:
        return []

    for obj in filter(lambda obj: obj.sollum_type in ANIM_SOLLUM_TYPES, objs):
        new_anim_obj: AnimObject = AnimObject(obj, 0, obj.sollum_type, False, False, [], False)
        anim_objs.append(new_anim_obj)
        draw_models: List[Object] = get_drawable_models_from_parent(obj)
        armature_action = get_action_from_armature(obj)
        if armature_action:
            new_anim_obj.skel_anims = True
            new_anim_obj.targets.append(Target(AnimationType.ARMATURE, obj, armature_action))

        if not draw_models:
            continue
        
        for child in draw_models:
            animated_mats: List[UvAnim] = get_data_from_materials(child)
            if animated_mats:
                new_anim_obj.uv_anims = True
                for data in animated_mats:
                    new_anim_obj.targets.append(Target(AnimationType.MATERIAL, data.material, data.action, data.material_idx))
                    
        new_anim_obj.flags = calc_basic_anim_flags(new_anim_obj.uv_anims, new_anim_obj.skel_anims, obj, obj.sollum_type)
                    
    return [anim for anim in anim_objs if anim.targets]

def calc_basic_anim_flags(uv_anims: bool, skel_anims: bool, obj: Object, sollum_type: str) -> int:
    """Calculate the basic animation flags for an animated object"""
    flags = 0
    match sollum_type:
        case "sollumz_drawable":
            if uv_anims:
                flags += 1024
            if skel_anims:
                flags += 512
        case "sollumz_fragment":
            flags += 131072 # dynamic flag
            if uv_anims:
                flags += 1024
            if skel_anims:
                flags += 512
    return flags
    
def get_drawable_models_from_parent(obj: Object) -> List[Object]:
    """Get all drawable models from a parent object"""
    child_drawable_list: List[Object] = []

    sollum_type: str = obj.sollum_type

    match sollum_type:
        case "sollumz_drawable":
            if obj.children:
                for child in obj.children:
                    if is_drawable_model(child):
                        child_drawable_list.append(child)
        case "sollumz_fragment":
            drawable = [child for child in obj.children if is_drawable(child)][0]
            if drawable:
                if drawable.children:
                    for child in drawable.children:
                        if is_drawable_model(child):
                            child_drawable_list.append(child)
                            
    return child_drawable_list

def get_data_from_materials(obj: Object) -> List[UvAnim]:
    """Get all actions and their corresponding materials from materials"""
    data: List[UvAnim] = []

    for idx, slot in enumerate(obj.material_slots):
        if slot.material.animation_data and slot.material.animation_data.action:
            data.append(UvAnim(slot.material, slot.material.animation_data.action, idx))

    return data

def get_action_from_armature(obj: Object) -> Action:
    """Get the action from an armature"""
    if obj.type == "ARMATURE":
        if obj.animation_data:
            return obj.animation_data.action
    return None

def create_ycd_obj(name: str) -> Object:
    """Create a YCD object"""
    ycd_parent = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(ycd_parent)
    ycd_parent.sollum_type = 'sollumz_clip_dictionary'
    return ycd_parent

def create_anim_tree(name: str) -> list:
    """Create the animation objects tree (Animations and Clips groups inside the Clip Dictionary object)"""
    ycd_parent = create_ycd_obj(name)
    animations_parent = create_ycd_groups(GroupType.ANIMATIONS)
    animations_parent.parent = ycd_parent
    clips_parent = create_ycd_groups(GroupType.CLIPS)
    clips_parent.parent = ycd_parent
    return [animations_parent, clips_parent]

def create_ycd_groups(enum: GroupType):
    parent = bpy.data.objects.new('parent', None)
    bpy.context.scene.collection.objects.link(parent)
    match enum:
        case GroupType.ANIMATIONS:
            parent.sollum_type = 'sollumz_animations'
            parent.name = 'Animations'
        case GroupType.CLIPS:
            parent.sollum_type = 'sollumz_clips'
            parent.name = 'Clips'
    return parent

def create_child(enum: ChildType, name: str = None) -> Object:
    """Create a child object"""
    child_obj = bpy.data.objects.new('new_child', None)
    if name:
        child_obj.name = name
    bpy.context.scene.collection.objects.link(child_obj)
    match enum:
        case ChildType.ANIMATION:
            child_obj.sollum_type = 'sollumz_animation'
        case ChildType.CLIP:
            child_obj.sollum_type = 'sollumz_clip'
    return child_obj

def get_arch_from_ytyps_by_obj(obj, scene):
    """Get the archetype from the YTYP(s) by object"""
    ytyps = scene.ytyps
    if len(ytyps) > 0:
        for ytyp in ytyps:
            if len(ytyp.archetypes) > 0:
                for archetype in ytyp.archetypes:
                    if archetype.asset == obj:
                        return archetype

def set_anim_properties(target: Target, anim_obj_empty: Object, target_obj: Object | None = None) -> None:
    """Set the animation properties for the sollum_animation object empty"""
    match target.target_id_type:
        case AnimationType.ARMATURE:
            anim_obj_empty.animation_properties.hash = target.target_id.name
            anim_obj_empty.animation_properties.target_id = target.target_id.data
            
        case AnimationType.MATERIAL:
            anim_obj_empty.animation_properties.hash = f"{target_obj.name}_uv_{target.material_idx}"
            anim_obj_empty.animation_properties.target_id = target.target_id
        case AnimationType.CAMERA:
            anim_obj_empty.animation_properties.hash = target.target_id.name
            anim_obj_empty.animation_properties.target_id = target.target_id.data

    anim_obj_empty.animation_properties.target_id_type = target.target_id_type.value
    anim_obj_empty.animation_properties.action = target.action
    
def set_clip_properties(target: Target, clip_obj_empty: Object, anim_obj_empty: Object, target_obj: Object | None = None) -> None:
    """Set the clip properties for the sollum_clip object empty"""
    match target.target_id_type:
        case AnimationType.ARMATURE:
            clip_obj_empty.clip_properties.hash = target_obj.name
            clip_obj_empty.clip_properties.name = f"{target_obj.name}.clip"
        case AnimationType.MATERIAL:
            clip_obj_empty.clip_properties.name = f"{target_obj.name}_uv_{target.material_idx}.clip"
            
    link_anim = clip_obj_empty.clip_properties.animations.add()
    link_anim.animation = anim_obj_empty
    action_duration = target.action.frame_range[1]
    clip_obj_empty.clip_properties.duration = action_duration / bpy.context.scene.render.fps