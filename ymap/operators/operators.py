import bpy
from ...vicho_dependencies import dependencies_manager as d
    
class VICHO_OT_open_folder(bpy.types.Operator):
    """Opens a generic windows folder dialog"""
    bl_idname = "ymap.open_folder"
    bl_label = "Open Folder"
    
    def execute(self, context):
        file_browser = d.FolderBrowser()
        result = file_browser.GetSelectedPath()
        if result:
            context.scene.ymap_assets_path = result if result else ""
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No path selected")
            return {'CANCELLED'}