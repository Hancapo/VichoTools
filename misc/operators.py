import bpy
from .funcs import add_transform_item, remove_transform_item_by_index, set_obj_to_transform_item, reset_transform_obj, get_top_parent

class IndexHelper:
    index: bpy.props.IntProperty()
    
class ContextActiveObjectRestrict:
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
class ContextActiveObjectParentRestrict:
    @classmethod
    def poll(cls, context):
        return context.active_object.parent is not None
    
class ContextActiveObjectTransformsRestrict:
    @classmethod
    def poll(cls, context):
        len(context.active_object.transforms_list) > 0
    
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
    
class TRANSFORMS_OT_transfer_to_parent(bpy.types.Operator):
    """Transfer transforms to top parent"""
    
    bl_idname = "transforms.transfer_to_parent"
    bl_label = "Transfer to Parent"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.parent is not None and len(context.active_object.transforms_list) > 0

    def execute(self, context):
        active_obj = context.active_object
        parent_obj = get_top_parent(active_obj)
        
        for trans in active_obj.transforms_list:
            new_transform = parent_obj.transforms_list.add()
            new_transform.name = trans.name
            new_transform.location = trans.location
            new_transform.rotation = trans.rotation
            new_transform.scale = trans.scale
            
        active_obj.transforms_list.clear()
        context.view_layer.objects.active = parent_obj
        parent_obj.select_set(True)
        
        return {'FINISHED'}