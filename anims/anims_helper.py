import bpy
from .enums import GroupType, ChildType, AnimationType
from ..misc.misc_funcs import is_object_in_scene, is_drawable_model

def create_anim_tree(name: str) -> list:
    ycd_parent = create_base_ycd_obj(name)
    animations_parent = create_ycd_groups(GroupType.ANIMATIONS)
    animations_parent.parent = ycd_parent
    clips_parent = create_ycd_groups(GroupType.CLIPS)
    clips_parent.parent = ycd_parent
    return [animations_parent, clips_parent]     

def create_anims_per_obj(anim_parent, objs):
    anim_mat_count = 0
    for obj in objs:
        if not is_object_in_scene(obj):
            continue
        if obj.type == 'EMPTY':
            if obj.children:
                for child in obj.children:
                    if is_drawable_model(child):
                        if not is_object_in_scene(child):
                            continue
                        child_name = child.name.split('.')[0]
                        for mat in child.material_slots:
                            print(f'Current material: {mat.material.name}')
                            child_mat = mat.material
                            if child_mat.sollum_type == 'sollumz_material_shader' and child_mat.animation_data:
                                mat_anim = create_child_group_obj(ChildType.ANIMATION, f'{child_name}_uv_{str(anim_mat_count)}')
                                mat_anim.parent = anim_parent
                                set_anim_props(mat_anim, mat_anim.name, child_mat.animation_data.action, child_mat, AnimationType.MATERIAL)
                                anim_mat_count += 1
                        anim_mat_count = 0
        elif obj.type == 'ARMATURE':
            if obj.sollum_type == 'sollumz_drawable' and obj.animation_data:
                skel_anim = create_child_group_obj(ChildType.ANIMATION, f'{obj.name}@anim')
                skel_anim.parent = anim_parent
                set_anim_props(skel_anim, skel_anim.name, obj.animation_data.action, obj.data, AnimationType.ARMATURE)
        else:
            continue
                
def create_clips_per_obj(anim_parent, clip_parent):
    for anim in anim_parent.children:
        clip_obj = create_child_group_obj(ChildType.CLIP, f'{anim.name.replace("@anim", "")}@clip')
        clip_obj.parent = clip_parent
        match anim.animation_properties.target_id_type:
            case 'MATERIAL':
                set_clip_props(clip_obj, f'{anim.name}.clip', anim.animation_properties.action.frame_range[1], AnimationType.MATERIAL)
            case 'ARMATURE':
                set_clip_props(clip_obj, f'{anim.name}.clip', anim.animation_properties.action.frame_range[1], AnimationType.ARMATURE)
        link_anim = clip_obj.clip_properties.animations.add()
        link_anim.animation = anim

def create_child_group_obj(enum: ChildType, name: str = None):
    child_obj = bpy.data.objects.new('_unk111', None)
    if name:
        child_obj.name = name
    bpy.context.scene.collection.objects.link(child_obj)
    match enum:
        case ChildType.ANIMATION:
            child_obj.sollum_type = 'sollumz_animation'
        case ChildType.CLIP:
            child_obj.sollum_type = 'sollumz_clip'
    return child_obj

def create_ycd_groups(enum: GroupType):
    unk_parent = bpy.data.objects.new('unknown', None)
    bpy.context.scene.collection.objects.link(unk_parent)
    match enum:
        case GroupType.ANIMATIONS:
            unk_parent.sollum_type = 'sollumz_animations'
            unk_parent.name = 'Animations'
        case GroupType.CLIPS:
            unk_parent.sollum_type = 'sollumz_clips'
            unk_parent.name = 'Clips'
    return unk_parent

def create_base_ycd_obj(name: str):
    ycd_parent = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(ycd_parent)
    ycd_parent.sollum_type = 'sollumz_clip_dictionary'
    return ycd_parent

def set_anim_props(obj, hash, action, target_id, enum: AnimationType):
    obj.animation_properties.hash = hash
    obj.animation_properties.action = action
    obj.animation_properties.target_id = target_id
    match enum:
        case AnimationType.ARMATURE:
            obj.animation_properties.target_id_type = 'ARMATURE'
            obj.animation_properties.hash = hash.replace('@anim', '')
        case AnimationType.MATERIAL:
            obj.animation_properties.target_id_type = 'MATERIAL'
            obj.animation_properties.hash = hash
        case AnimationType.CAMERA:
            obj.animation_properties.target_id_type = 'CAMERA'

def set_clip_props(obj, name, anim_duration, enum: AnimationType):
    fps = bpy.context.scene.render.fps
    obj.clip_properties.duration = anim_duration / fps
    match enum:
        case AnimationType.ARMATURE:
            obj.clip_properties.hash = obj.name.replace('@clip', '')
            obj.clip_properties.name = name.replace('@anim', '')
        case AnimationType.MATERIAL:
            obj.clip_properties.hash = obj.name
            obj.clip_properties.name = name