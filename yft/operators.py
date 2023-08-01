import bpy

from .yft_helper import assign_bone_flags_to_selection, create_child_by_cols, create_sollumz_armature, create_sollumz_drawable

class CreateFragChildsFromCols(bpy.types.Operator):
    bl_idname = "vicho.createfragchildsfromcols"
    bl_label = "Create Frag Childs from COLs"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None
    
    def execute(self, context):
        scene = context.scene
        objects = context.selected_objects
        create_child_by_cols(objects, scene, scene.material_density)
        return {'FINISHED'}

class BoneFlagsToSelectedBones(bpy.types.Operator):
    bl_idname = "vicho.boneflagstoselectedbones"
    bl_label = "Bone Flags to selected bones"

    @classmethod
    def poll(cls, context):
        return context.active_object.type == 'ARMATURE'
    
    def execute(self, context):
        scene = context.scene
        armature = context.active_object
        assign_bone_flags_to_selection(armature, scene)
        return {'FINISHED'}
    
class CreateArmatureFromSelection(bpy.types.Operator):
    bl_idname = "vicho.createarmaturefromselection"
    bl_label = "Create Armature from selection"

    @classmethod
    def poll(cls, context):
        return context.selected_objects is not None
    
    def execute(self, context):
        scene = context.scene
        objects = context.selected_objects
        converted_objects = []
        for obj in objects:
            converted_objects.append(create_sollumz_drawable(obj))
        
        create_sollumz_armature(converted_objects, True, scene.create_multiple_yft, scene.bone_id_gen)
        return {'FINISHED'}