import bpy
from .operators import VICHO_OT_import_ymap
from ..vicho_dependencies import dependencies_manager as dm
from .funcs import get_ymap_name

class YMAPLIST_UL_list(bpy.types.UIList):
    bl_idname = "YMAPLIST_UL_list"
    
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            ymap_list = dm.ymap_list
            if ymap_list:
                ymap = ymap_list[index]
                ymap_name = get_ymap_name(ymap)
                layout.prop(item, "enabled", text="", emboss=False, icon="CHECKBOX_HLT" if item.enabled else "CHECKBOX_DEHLT")
                layout.label(text=ymap_name, icon="MEMORY")
                
class YmapTools_PT_Panel(bpy.types.Panel):
    bl_label = "Map Data"
    bl_idname = "VICHOTOOLS_PT_Ymap"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vicho's Tools"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        self.layout.label(text="", icon="FORCE_MAGNETIC")
        
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        col = layout.column(align=True)
        
        col.template_list(YMAPLIST_UL_list.bl_idname, "", scene, "ymap_list", scene, "ymap_list_index")
        
        col = layout.column(align=True)
        col.operator(VICHO_OT_import_ymap.bl_idname, text="Import YMAP")
        col.separator()
        col.prop(bpy.context.scene, "ymap_assets_path")
