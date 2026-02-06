import bpy
from ..icons_load import get_icon
from .operators import VICHO_OT_start_asset_server, VICHO_OT_load_game_files
from ..vicho_dependencies import dependencies_manager as d

class AssetImporterPanel(bpy.types.Panel):
    bl_label = "Asset Importer"
    bl_idname = "VICHOTOOLS_PT_AssetImporter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vicho's Tools"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        self.layout.label(text="", icon_value=get_icon("database_marker"))
        
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        is_server_running = scene.is_vicho_server_running
        col = layout.column()
        row = col.row()
        col1 = layout.column()
        row1 = col1.row()
        
        if d.gamecache:
            row1.enabled = False
            row.enabled = True
        
        row1.operator(VICHO_OT_load_game_files.bl_idname, text="Load Game Files")
        
        row.alert = is_server_running
        row.operator(VICHO_OT_start_asset_server.bl_idname, text="Stop Server" if is_server_running else "Start server")
        row.prop(context.scene, "add_asset_to_scene", text="Add Entity to Scene")
        
        header, panel = layout.panel("_server_vicho_settings", default_closed=True)
        
        header.label(text= "Server Settings", icon="INTERNET")
        if panel:
            panel_col = panel.column()
            panel_col.prop(context.scene, "asset_ip", text="IP")
            panel_col.prop(context.scene, "asset_port", text="Port")
        
        