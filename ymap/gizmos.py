import bpy
from mathutils import Matrix, Vector

def get_extents_matrix(context, type):
        selected_ymap = context.scene.fake_ymap_list[context.scene.ymap_list_index]
        match type:
            case 'streaming':
                min_x, min_y, min_z = selected_ymap.streaming_extents_min
                max_x, max_y, max_z = selected_ymap.streaming_extents_max
            case 'entities':
                min_x, min_y, min_z = selected_ymap.entities_extents_min
                max_x, max_y, max_z = selected_ymap.entities_extents_max
        
        min_coords = Vector((min_x, min_y, min_z))
        max_coords = Vector((max_x, max_y, max_z))
        
        center = (min_coords + max_coords) / 2
        
        dimensions = max_coords - min_coords
        
        scale_matrix = Matrix.Scale(dimensions.x, 4, Vector((1, 0, 0))) @ \
               Matrix.Scale(dimensions.y, 4, Vector((0, 1, 0))) @ \
               Matrix.Scale(dimensions.z, 4, Vector((0, 0, 1)))
               
        translate_matrix = Matrix.Translation(center)
        
        return translate_matrix @ scale_matrix

class StreamingExtentsGizmoGroup(bpy.types.GizmoGroup):
    bl_idname = "OBJECT_GGT_Streaming_Extents"
    bl_label = "Streaming Extents Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT', 'DEPTH_3D'}
    
    @classmethod
    def poll(cls, context):
        ymap_index = context.scene.ymap_list_index
        if ymap_index != -1:
            if len(context.scene.fake_ymap_list) > 0:
                selected_ymap = context.scene.fake_ymap_list[context.scene.ymap_list_index]
                return selected_ymap.show_streaming_extents
    
    
    def setup(self, context):
        gizmo_entities = self.gizmos.new("GIZMO_GT_cage_3d")
        gizmo_entities.color = (0.4, 0.7, 0.0)
        gizmo_entities.line_width = 4
        gizmo_entities.draw_style = 'BOX'
        gizmo_entities.matrix_offset = get_extents_matrix(context, 'streaming')
        
    def refresh(self, context):
        if context.scene.ymap_list_index != -1:
            for gizmo in self.gizmos:
                gizmo.matrix_offset = get_extents_matrix(context, 'streaming')
                    
class EntitiesExtentsGizmoGroup(bpy.types.GizmoGroup):
    bl_idname = "OBJECT_GGT_Entities_Extents"
    bl_label = "Entities Extents Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT', 'DEPTH_3D'}
    
    @classmethod
    def poll(cls, context):
        ymap_index = context.scene.ymap_list_index
        if ymap_index != -1:
            if len(context.scene.fake_ymap_list) > 0:
                selected_ymap = context.scene.fake_ymap_list[context.scene.ymap_list_index]
                return selected_ymap.show_entities_extents
    
    
    def setup(self, context):
        gizmo_entities = self.gizmos.new("GIZMO_GT_cage_3d")
        gizmo_entities.color = (0.7, 0.4, 1.0)
        gizmo_entities.line_width = 1
        gizmo_entities.draw_style = 'BOX'
        gizmo_entities.matrix_offset = get_extents_matrix(context, 'entities')
        
    def refresh(self, context):
        if context.scene.ymap_list_index != -1:
            for gizmo in self.gizmos:
                gizmo.matrix_offset = get_extents_matrix(context, 'entities')