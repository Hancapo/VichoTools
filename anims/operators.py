import bpy
from .anims_helper import create_anim_tree, create_animations_per_object, order_sollumz_shaders, create_clips_per_object

class AnimCreateUVAnimsFromSelected(bpy.types.Operator):
    """Create UV animations from selected objects"""
    bl_idname = "anim.create_uv_anims_from_selected"
    bl_label = "Create UV animations from selected objects and its materials"

    @classmethod
    def poll(cls, context):
        return any(obj.sollum_type == 'sollumz_drawable' for obj in bpy.context.selected_objects) and bpy.context.scene.ycd_name != ""

    def execute(self, context):
        scene = context.scene

        sel_objs = bpy.context.selected_objects

        #if order_sollumz_shaders(sel_objs):
        self.report({'INFO'}, 'Shaders ordered successfully for selected objects')
        anim_ycd: list = create_anim_tree(scene.ycd_name)
        create_animations_per_object(anim_ycd[0], sel_objs)
        create_clips_per_object(anim_ycd[0], anim_ycd[1])

        return {'FINISHED'}