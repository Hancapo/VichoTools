import bpy
from .helper import load_gta_cache, get_file_folder_list
from ..vicho_dependencies import dependencies_manager as d
import pathlib
import os

class ExportAssetsFromFile(bpy.types.Operator):
    bl_idname = "rpf.export_assets_from_file"
    bl_label = "Export Assets from File"
    bl_description = "Export Assets from File"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}
    
class RPFLoadGTA5(bpy.types.Operator):
    bl_idname = "rpf.load_gta5"
    bl_label = "Load GTA5"
    bl_description = "Load GTA5"
    bl_options = {'REGISTER', 'UNDO'}
    
    directory: bpy.props.StringProperty(subtype="DIR_PATH", description="Select your GTAV Path" ,default="")
    
    @classmethod
    def poll(cls, context):
        return d.gamecache is None

    def execute(self, context):
        if load_gta_cache(self.directory):
            get_file_folder_list(context.scene.file_list, self.directory)
            context.scene.file_list_current_path = self.directory
            self.report({'INFO'}, "GTA5 Files loaded successfully")
        else:
            self.report({'ERROR'}, "Error loading GTA5 Files")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
class RPFOpenFolder(bpy.types.Operator):
    """Open Folder"""

    bl_idname = "rpf.openfolder"
    bl_label = ""

    item_id: bpy.props.StringProperty()

    def execute(self, context):
        scene = context.scene
        for _, item in enumerate(scene.file_list):
            if item.id == self.item_id:
                if item.file_type == "FOLDER":
                    item_copy = item
                    folder_path = pathlib.Path(item_copy.path)
                    print(f"Opening folder: {folder_path}")
                    context.scene.file_list.clear()
                    get_file_folder_list(scene.file_list, str(folder_path))
                    scene.file_list_current_path = str(folder_path)
                    break
                if item.file_type == "RPF":
                    print(f"Opening RPF: {item.name}")
                    break
        
        return {"FINISHED"}
    
class RPFBackFolder(bpy.types.Operator):
    """Back Folder"""

    bl_idname = "rpf.backfolder"
    bl_label = ""
    
    @classmethod
    def poll(cls, context):
        flcp = context.scene.file_list_current_path
        return pathlib.Path(flcp).name != 'Grand Theft Auto V'

    def execute(self, context):
        scene = context.scene
        scene.file_list.clear()
        get_file_folder_list(scene.file_list, pathlib.Path(scene.file_list_current_path).parent)
        scene.file_list_current_path = str(pathlib.Path(scene.file_list_current_path).parent)
        return {"FINISHED"}