from .operators_ymap import YmapData
import bpy


class VICHO_OT_add_phys_dict(bpy.types.Operator, YmapData):
    """Adds a new physical dictionary to the YMAP"""
    bl_idname = "ymap.add_phys_dict"
    bl_label = "Add Physical Dictionary"
    
    @classmethod
    def poll(cls, context):
        return context.scene.ymap_list and context.scene.ymap_list_index >= 0

    def execute(self, context):
        ymap = self.get_ymap(context)
        new_pd = ymap.ymap_phys_dicts.add()
        new_pd.name = "New Physical Dictionary"
        return {'FINISHED'}
    
class VICHO_OT_remove_phys_dict(bpy.types.Operator, YmapData):
    """Removes the selected physics dictionary from the YMAP"""
    bl_idname = "ymap.remove_phys_dict"
    bl_label = "Remove Physics Dictionary"
    
    @classmethod
    def poll(cls, context):
        return len(context.scene.ymap_list[context.scene.ymap_list_index].ymap_phys_dicts) > 0

    def execute(self, context):
        ymap = self.get_ymap(context)
        if ymap.ymap_phys_dicts:
            pds = ymap.ymap_phys_dicts
            pds.remove(ymap.ymap_phys_dicts_index)
            ymap.ymap_phys_dicts_index = max(0, ymap.ymap_phys_dicts_index - 1)
            self.report({'INFO'}, "Physics dictionary removed")
        else:
            self.report({'WARNING'}, "No Physics dictionaries to remove")

        return {'FINISHED'} 