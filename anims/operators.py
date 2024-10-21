import bpy
from .helper import (get_anim_objs_from_sel, 
                         create_anim_tree, 
                         create_child, 
                         set_anim_properties, 
                         set_clip_properties,
                         get_arch_from_ytyps_by_obj)

from ..misc.constants import ANIM_SOLLUM_TYPES
from .enums import ChildType, AnimationType

class CreateClipDictionaryFromSelected(bpy.types.Operator):
    """Create a YCD from selected objects"""
    bl_idname = "anim.create_anims_from_selected"
    bl_label = "Create a YCD from selected objects"

    @classmethod
    def poll(cls, context):
        return any(obj.sollum_type in ANIM_SOLLUM_TYPES for obj in context.selected_objects) and context.scene.ycd_name != ""

    def execute(self, context):
        scene = context.scene
        
        autofill: bool = scene.autofill_clipdict
        calc_anim_flags: bool = scene.calculate_anim_flags
        auto_start: bool = scene.auto_start_anim_flag
        ycd_name: str = scene.ycd_name
        
        sel_objs = bpy.context.selected_objects
        anim_list = get_anim_objs_from_sel(sel_objs)
        print(anim_list)
        
        if not anim_list:
            self.report({'ERROR'}, "No animated objects found")
            return {'FINISHED'}
        else:
            self.report({'INFO'}, f"Found {len(anim_list)} animated objects")
            anim_group, clip_group = create_anim_tree(ycd_name)
            for anim_obj in anim_list:
                for i, target in enumerate(anim_obj.targets):
                    match target.target_id_type:
                        case AnimationType.ARMATURE:
                            anim_naming = f"{anim_obj.obj.name}@skel_anim_{i}"
                            clip_naming = f"{anim_obj.obj.name}@skel_clip_{i}"
                        case AnimationType.MATERIAL:
                            anim_naming = f"{anim_obj.obj.name}@uv_anim_{target.material_idx}"
                            clip_naming = f"{anim_obj.obj.name}@uv_clip_{target.material_idx}"
                    # Create Animation
                    new_anim = create_child(ChildType.ANIMATION, anim_naming)
                    new_anim.parent = anim_group
                    set_anim_properties(target, new_anim, anim_obj.obj)
                    # Create Clip
                    new_clip = create_child(ChildType.CLIP, clip_naming)
                    new_clip.parent = clip_group
                    set_clip_properties(target, new_clip, new_anim, anim_obj.obj)
                
                arch = get_arch_from_ytyps_by_obj(anim_obj.obj, scene)
                if arch:
                    if autofill:
                        arch.clip_dictionary = ycd_name
                    if calc_anim_flags:
                        arch.flags.total = str(anim_obj.flags)
                    if auto_start:
                        arch.flags.total = str(int(arch.flags.total) + 524288)
                    
            self.report({'INFO'}, f"Created {len(anim_obj.targets)} Animation(s)/Clip(s)")
            
        
        return {'FINISHED'}