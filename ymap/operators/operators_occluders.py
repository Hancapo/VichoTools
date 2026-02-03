import bpy
from ..ymap_mixin import YmapMixin
from bpy.types import Object
from ...shared.helper import is_mesh_a_cube, assign_mat, create_cube_obj
from ..helper import box_occluder_mat, occluder_model_mat, create_box_occluder_item


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
        if self.has_occluders(context):
            box_occls = self.get_ymap_box_occls(context)
            box_occls.remove(YmapMixin.get_ymap_box_occl_index(context))
            self.report({'INFO'}, f"Removed box occlusion culling object from {self.get_ymap(context).ymap_object.name} YMAP")
            return {'FINISHED'}

class YMAP_OT_create_model_occluder(bpy.types.Operator, YmapMixin):
    """Creates a model occlusion culling object in the currently selected YMAP"""
    bl_idname = "ymap.create_model_occluder"
    bl_label = "Create Model Occluder"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return cls.get_ymap(context) is not None

    ...


class YMAP_OT_remove_model_occluder(bpy.types.Operator, YmapMixin):
    """Removes a model occlusion culling object from the currently selected YMAP"""
    bl_idname = "ymap.remove_model_occluder"
    bl_label = "Remove Model Occluder"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return cls.has_occluders(context) > 0 and cls.get_ymap_model_occl_index(context) > -1

    ...