import bpy
from .helper import add_transform_item, remove_transform_item_by_index, set_obj_to_transform_item, any_transform_items
from ..shared.helper import reset_obj_transform, get_top_parent, is_active_obj, obj_has_parent, get_active_obj, IndexHelper
from ..shared.funcs import poll_all


    
class TRANSFORMS_OT_add(bpy.types.Operator):
    """Add a new transform"""
    bl_idname = "transforms.add"
    bl_label = "Add Transform"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_all(context, is_active_obj)

    def execute(self, context):
        add_transform_item(self, context)
        return {'FINISHED'}

class TRANSFORMS_OT_remove(bpy.types.Operator, IndexHelper):
    """Remove the selected transform"""
    bl_idname = "transforms.remove"
    bl_label = "Remove Transform"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_all(context, is_active_obj)

    def execute(self, context):
        remove_transform_item_by_index(self, context, self.index)
        return {'FINISHED'}
        
class TRANSFORMS_OT_set(bpy.types.Operator, IndexHelper):
    """Set the object to the selected transform"""
    bl_idname = "transforms.set"
    bl_label = "Set Transform"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_all(context, is_active_obj)
    
    def execute(self, context):
        set_obj_to_transform_item(self, context, self.index)
        return {'FINISHED'}
    
class TRANSFORMS_OT_reset(bpy.types.Operator):
    """Reset all transforms"""
    
    bl_idname = "transforms.reset"
    bl_label = "Reset Transforms"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_all(context, is_active_obj)
    
    def execute(self, context):
        reset_obj_transform(get_active_obj())
        return {'FINISHED'}
    
class TRANSFORMS_OT_transfer_to_parent(bpy.types.Operator):
    """Transfer transforms to top parent"""
    
    bl_idname = "transforms.transfer_to_parent"
    bl_label = "Transfer to Parent"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return poll_all(context, is_active_obj, obj_has_parent, any_transform_items)

    def execute(self, context):
        active_obj = get_active_obj()
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