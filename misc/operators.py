import bpy
from .funcs import add_transform_item, remove_transform_item_by_index, set_obj_to_transform_item, reset_transform_obj

class IndexHelper:
    index: bpy.props.IntProperty()
    
class ContextActiveObjectRestrict:
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

class TRANSFORMS_OT_add(bpy.types.Operator, ContextActiveObjectRestrict):
    """Add a new transform"""
    bl_idname = "transforms.add"
    bl_label = "Add Transform"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        add_transform_item(self, context)
        return {'FINISHED'}

class TRANSFORMS_OT_remove(bpy.types.Operator, IndexHelper, ContextActiveObjectRestrict):
    """Remove the selected transform"""
    bl_idname = "transforms.remove"
    bl_label = "Remove Transform"
    bl_options = {'REGISTER', 'UNDO'}
    

    def execute(self, context):
        remove_transform_item_by_index(self, context, self.index)
        return {'FINISHED'}
        
class TRANSFORMS_OT_set(bpy.types.Operator, IndexHelper, ContextActiveObjectRestrict):
    """Set the object to the selected transform"""
    bl_idname = "transforms.set"
    bl_label = "Set Transform"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        set_obj_to_transform_item(self, context, self.index)
        return {'FINISHED'}
    
class TRANSFORMS_OT_reset(bpy.types.Operator, ContextActiveObjectRestrict):
    """Reset all transforms"""
    
    bl_idname = "transforms.reset"
    bl_label = "Reset Transforms"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        reset_transform_obj(self, context)
        return {'FINISHED'}