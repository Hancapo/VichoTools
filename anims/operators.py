import bpy
from .anims_helper import create_anim_tree, create_clips_per_obj, create_anims_per_obj

class CreateClipDictionaryFromSelected(bpy.types.Operator):
    """Create YCD from selected objects"""
    bl_idname = "anim.create_anims_from_selected"
    bl_label = "Create YCD from selected objects"

    @classmethod
    def poll(cls, context):
        return any(obj.sollum_type == 'sollumz_drawable' for obj in bpy.context.selected_objects) and bpy.context.scene.ycd_name != ""

    def execute(self, context):
        scene = context.scene
        sel_objs = bpy.context.selected_objects
        anim_ycd: list = create_anim_tree(scene.ycd_name)
        create_anims_per_obj(anim_ycd[0], sel_objs)
        create_clips_per_obj(anim_ycd[0], anim_ycd[1])
        return {'FINISHED'}