import bpy
from .anims_helper import create_anim_tree, create_clips_per_obj, create_anims_per_obj, get_targets_from_anim, sutchis_from_tgt, get_arch_from_ytyps_by_obj, calculate_anim_flags

class CreateClipDictionaryFromSelected(bpy.types.Operator):
    """Create YCD from selected objects"""
    bl_idname = "anim.create_anims_from_selected"
    bl_label = "Create YCD from selected objects"

    @classmethod
    def poll(cls, context):
        return any(obj.sollum_type == 'sollumz_drawable' or 'sollumz_fragment' for obj in bpy.context.selected_objects) and bpy.context.scene.ycd_name != ""

    def execute(self, context):
        scene = context.scene
        
        autofill: bool = scene.autofill_clipdict
        calc_anim_flags: bool = scene.calculate_anim_flags
        auto_start: bool = scene.auto_start_anim_flag
        
        sel_objs = bpy.context.selected_objects
        anim_ycd: list = create_anim_tree(scene.ycd_name)
        create_anims_per_obj(anim_ycd[0], sel_objs)
        create_clips_per_obj(anim_ycd[0], anim_ycd[1])
        
        if autofill:
            created_ycd = scene.objects[scene.ycd_name]
            targets = get_targets_from_anim(created_ycd)
            print(f'targets found: {targets}')
            for target in targets:
                sutchi = sutchis_from_tgt(target, scene)
                print(f'Found sutchi: {sutchi}')
                arch = get_arch_from_ytyps_by_obj(sutchi.object, scene)
                if arch:
                    arch.clip_dictionary = scene.ycd_name
                    if calc_anim_flags:
                        static_flag = 0
                        if arch.physics_dictionary != "":
                            static_flag = 32
                        arch.flags.total = str(calculate_anim_flags(auto_start, sutchi.sol_type, sutchi.flags) + static_flag)
        
        return {'FINISHED'}