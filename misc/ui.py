import bpy
from .operators import TRANSFORMS_OT_add, TRANSFORMS_OT_remove, TRANSFORMS_OT_reset


class TRANSFORMS_UL_list(bpy.types.UIList):
    bl_idname = "TRANSFORMS_UL_list"
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "name", text="", emboss=False, icon='OBJECT_DATA')
            layout.operator(TRANSFORMS_OT_remove.bl_idname, text="", icon='X', emboss=False).index = index
            
class TransformsManagerTools_PT_Panel(bpy.types.Panel):
    bl_label = "Transforms Manager"
    bl_idname = "TRANSFORMS_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Tools"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "VICHOTOOLS_PT_Object"
    
    def draw_header(self, context):
        self.layout.label(text="", icon="ORIENTATION_GIMBAL")
        
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        obj = context.object
        scene = context.scene
        
        if obj:
            col.label(text=f"{obj.name} selected.", icon='OBJECT_DATA')
            row = col.row(align=True)
            row.template_list(TRANSFORMS_UL_list.bl_idname, "", obj, "transforms_list", obj, "active_transform_index")
            col2 = col.column(align=True)
            row2 = col2.row(align=True)
            row2.operator(TRANSFORMS_OT_add.bl_idname, text="", icon='ADD')
            row2.prop(scene, "lock_transform", text="Lock Transforms", icon='TRIA_RIGHT')
            row2.operator(TRANSFORMS_OT_reset.bl_idname, text="Reset Transform from Object", icon='FILE_REFRESH')
        else:
            row.label(text="No object selected", icon='ERROR')
