import bpy

def create_anim_tree(name: str) -> list:
    ycd_parent = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(ycd_parent)
    ycd_parent.sollum_type = 'sollumz_clip_dictionary'

    animations_parent = bpy.data.objects.new('Animations', None)
    bpy.context.scene.collection.objects.link(animations_parent)
    animations_parent.sollum_type = 'sollumz_animations'
    animations_parent.parent = ycd_parent

    clips_parent = bpy.data.objects.new('Clips', None)
    bpy.context.scene.collection.objects.link(clips_parent)
    clips_parent.sollum_type = 'sollumz_clips'
    clips_parent.parent = ycd_parent

    return [animations_parent, clips_parent]

def order_sollumz_shaders(objs):
    Success = True
    for obj in objs:
        if obj.sollum_type == 'sollumz_drawable':
            with bpy.context.temp_override(aobj=obj):
                result = bpy.ops.sollumz.order_shaders()
                if 'FINISHED' not in result:
                    Success = False
    return Success


def create_animations_per_object(anim_parent, objs):
    anim_count = 0
    valid_child = [child for obj in objs for child in obj.children if child.sollum_type == 'sollumz_drawable_model']
    for obj in valid_child:
        obj_name = obj.name.split('.')[0]
        for mat in obj.material_slots:
            obj_mat = mat.material
            if obj_mat.sollum_type == 'sollumz_material_shader' and obj_mat.animation_data:
                mat_anim = bpy.data.objects.new(f'{obj_name}_{str(anim_count)}@anim', None)
                bpy.context.scene.collection.objects.link(mat_anim)
                mat_anim.sollum_type = 'sollumz_animation'
                mat_anim.parent = anim_parent
                mat_anim.animation_properties.hash = obj_name
                mat_anim.animation_properties.action = obj_mat.animation_data.action
                mat_anim.animation_properties.target_id_type = 'MATERIAL'
                mat_anim.animation_properties.target_id = obj_mat
                anim_count += 1
        anim_count = 0        

def create_clips_per_object(anim_parent, clip_parent):
    for anim in anim_parent.children:
        clip_obj = bpy.data.objects.new(anim.name.replace('anim', 'clip'), None)
        bpy.context.scene.collection.objects.link(clip_obj)
        clip_obj.sollum_type = 'sollumz_clip'
        clip_obj.parent = clip_parent
        clip_obj.clip_properties.name = anim.name.replace('anim', 'clip').replace('@', '.')
        clip_obj.clip_properties.duration = anim.animation_properties.action.frame_range[1] / bpy.context.scene.render.fps
        link_anim = clip_obj.clip_properties.animations.add()
        link_anim.animation = anim