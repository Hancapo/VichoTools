import bpy
from .operators import VICHO_OT_import_ymap

class YMAPLIST_UL_list(bpy.types.UIList):
    bl_idname = "YMAPLIST_UL_list"
    
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.row(align=True)
            row.prop(item, "name", text="", emboss=False, icon="ASSET_MANAGER")


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
        col = layout.column(align=True)
        
        col.template_list(YMAPLIST_UL_list.bl_idname, "", context.scene, "ymap_list", context.scene, "ymap_list_index")
        
        col = layout.column(align=True)
        col.operator(VICHO_OT_import_ymap.bl_idname, text="Import YMAP")
        col.prop(bpy.context.scene, "ymap_assets_path")
