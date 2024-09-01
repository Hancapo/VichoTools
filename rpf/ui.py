import bpy
from .operators import ExportAssetsFromFile, RPFLoadGTA5, RPFOpenFolder, RPFBackFolder
from .helper import get_folder_file_icon

class RPF_PT_UI(bpy.types.Panel):
    bl_label = "RPF"
    bl_idname = "RPF_PT_UI"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Tools"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        self.layout.label(text="", icon="WORLD_DATA")

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        col = row.column(align=True)
        col.operator(ExportAssetsFromFile.bl_idname, text="Export Assets from File", icon="EXPORT")
        col.operator(RPFLoadGTA5.bl_idname, text="Load GTA5", icon="IMPORT")
        
        row = layout.row()
        col = row.column(align=True)
        
        col.operator(RPFBackFolder.bl_idname, text="", icon="BACK")
        col = row.column(align=True)
        col.template_list("FILEEXPLORER_UL_list", "", context.scene, "file_list", context.scene, "file_list_index")
        
class FILEEXPLORER_UL_list(bpy.types.UIList):
    bl_idname = "FILEEXPLORER_UL_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.row(align=True)
            if item.file_type in ["FOLDER", "RPF"]:
                op = row.operator(RPFOpenFolder.bl_idname, text="", icon="FORWARD")
                op.item_id = item.id
            row.label(text=item.name, icon=get_folder_file_icon(item.file_type))