import bpy
from ...shared.helper import get_path_from_folder_dialog
    
class VICHO_OT_open_folder(bpy.types.Operator):
    """Opens a generic windows folder dialog"""
    bl_idname = "ymap.open_folder"
    bl_label = "Open Folder"
    
    def execute(self, context):
        result = get_path_from_folder_dialog()
        if result:
            context.scene.ymap_assets_path = result if result else ""
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No path selected")
            return {'CANCELLED'}