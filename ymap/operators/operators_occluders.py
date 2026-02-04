import bpy
from ..ymap_mixin import YmapMixin
from bpy.types import Object
from ...shared.helper import is_mesh_a_cube, create_cube_obj, delete_obj
from ..helper import create_box_occluder_item, create_occluder_model_item


class YMAP_OT_create_box_occluder(bpy.types.Operator, YmapMixin):
    """Creates a box occlusion culling object in the currently selected YMAP"""
    bl_idname = "ymap.create_box_occluder"
    bl_label = "Create Box Occluder"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return cls.get_ymap(context) is not None
    
    def execute(self, context):
        box_objs: list[Object] = [obj for obj in context.selected_objects if is_mesh_a_cube(obj)]
        ymap, ymap_box_occl_group  = self.get_ymap(context), self.get_ymap_box_occl_group_obj(context)
        if len(box_objs) > 0:
            for box_obj in box_objs:
                if box_obj not in [occl.linked_obj for occl in ymap.ymap_box_occluders]:
                    create_box_occluder_item(box_obj, ymap, ymap_box_occl_group)
                else:
                    self.report({'WARNING'}, f"{box_obj.name} is already a box occlusion culling object in {ymap.ymap_object.name} YMAP")
                    return {'CANCELLED'}
            self.report({'INFO'}, f"Created {len(box_objs)} box occlusion culling objects in {ymap.ymap_object.name} YMAP")
            return {'FINISHED'}
        else:
            box_obj = create_cube_obj()
            if box_obj not in [occl.linked_obj for occl in ymap.ymap_box_occluders]:
                create_box_occluder_item(box_obj, ymap, ymap_box_occl_group)
                self.report({'INFO'}, f"Created box occlusion culling object in {ymap.ymap_object.name} YMAP")
                return {'FINISHED'}


class YMAP_OT_remove_box_occluder(bpy.types.Operator, YmapMixin):
    """Removes a box occlusion culling object from the currently selected YMAP"""
    bl_idname = "ymap.remove_box_occluder"
    bl_label = "Remove Box Occluder"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return cls.has_occluders(context) > 0 and cls.get_ymap_box_occl_index(context) > -1

    def execute(self, context):
        ymap = self.get_ymap(context)
        if self.has_occluders(context):
            index: int = self.get_ymap_box_occl_index(context)
            box_occls = ymap.ymap_box_occluders
            delete_obj(box_occls[index].linked_obj)
            box_occls.remove(index)
            ymap.ymap_box_occluders_index = max(0, index - 1)
            if len(box_occls) == 0:
                ymap.ymap_box_occluders_group_object = None
                delete_obj(self.get_ymap_box_occl_group_obj(context))
            if not self.has_occluders(context):
                ymap.ymap_occluders_group_object = None
                delete_obj(self.get_ymap_occl_group_obj(context))
            self.report({'INFO'}, f"Removed box occlusion culling object from {ymap.ymap_object.name} YMAP")
            return {'FINISHED'}

class YMAP_OT_create_model_occluder(bpy.types.Operator, YmapMixin):
    """Creates a model occlusion culling object in the currently selected YMAP"""
    bl_idname = "ymap.create_model_occluder"
    bl_label = "Create Model Occluder"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return cls.get_ymap(context) is not None

    def execute(self, context):
        model_objs: list[Object] = [obj for obj in context.selected_objects if obj.type == "MESH"]
        ymap, ymap_model_occl_group  = self.get_ymap(context), self.get_ymap_model_occl_group_obj(context)
        if len(model_objs) > 0:
            for model_obj in model_objs:
                if model_obj not in [occl.linked_obj for occl in ymap.ymap_model_occluders]:
                    create_occluder_model_item(model_obj, ymap, ymap_model_occl_group)
                else:
                    self.report({'WARNING'}, f"{model_obj.name} is already a model occlusion culling object in {ymap.ymap_object.name} YMAP")
                    return {'CANCELLED'}
            self.report({'INFO'}, f"Created {len(model_objs)} model occlusion culling objects in {ymap.ymap_object.name} YMAP")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "No object(s) selected")
            return {'CANCELLED'}


class YMAP_OT_remove_model_occluder(bpy.types.Operator, YmapMixin):
    """Removes a model occlusion culling object from the currently selected YMAP"""
    bl_idname = "ymap.remove_model_occluder"
    bl_label = "Remove Model Occluder"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return cls.has_occluders(context) > 0 and cls.get_ymap_model_occl_index(context) > -1

    def execute(self, context):
        ymap = self.get_ymap(context)
        if self.has_occluders(context):
            index: int = self.get_ymap_model_occl_index(context)
            model_occls = ymap.ymap_model_occluders
            delete_obj(model_occls[index].linked_obj)
            model_occls.remove(index)
            ymap.ymap_model_occluders_index = max(0, index - 1)
            if len(model_occls) == 0:
                ymap.ymap_model_occluders_group_object = None
                delete_obj(self.get_ymap_model_occl_group_obj(context))
            if not self.has_occluders(context):
                ymap.ymap_occluders_group_object = None
                delete_obj(self.get_ymap_occl_group_obj(context))
            self.report({'INFO'}, f"Removed model occlusion culling object from {ymap.ymap_object.name} YMAP")
            return {'FINISHED'}