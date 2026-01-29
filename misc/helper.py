import importlib
import subprocess
import traceback
from bpy.types import Object
from ..shared.helper import get_active_obj, zoom_to_objs
import shutil

def add_transform_item(self, context):
    obj: Object = context.active_object
    if obj:
        new_transform = obj.transforms_list.add()
        new_transform.name = f"Transform {len(obj.transforms_list)}"
        new_transform.location = obj.location.copy()
        obj.rotation_mode = 'XYZ'
        new_transform.rotation = obj.rotation_euler.copy()
        new_transform.scale = obj.scale.copy()
        obj.active_transform_index = len(obj.transforms_list) - 1
        return new_transform
    
def remove_transform_item_by_index(self, context, index) -> None:
    obj: Object = get_active_obj()
    if obj and obj.transforms_list:
        if 0 <= index < len(obj.transforms_list):
            obj.transforms_list.remove(index)
            if any_transform_items():
                obj.active_transform_index = min(obj.active_transform_index, len(obj.transforms_list) - 1)
            else:
                obj.active_transform_index = -1
    return None

def set_obj_to_transform_item(self, context, index) -> bool:
    obj: Object = get_active_obj()
    if obj and obj.transforms_list:
        if 0 <= index < len(obj.transforms_list):
            transform_item = obj.transforms_list[index]
            obj.location = transform_item.location
            obj.rotation_euler = transform_item.rotation
            obj.scale = transform_item.scale
            return True
    return False

def update_transform_index(self, context) -> None:
    if context.scene.lock_transform:
        return
    set_obj_to_transform_item(self, context, self.active_transform_index)
    obj = get_active_obj()
    obj.select_set(True)
    
    if context.scene.zoom_to_object:
        zoom_to_objs()
                    
def any_transform_items() -> bool:
    active_obj = get_active_obj()
    return active_obj is not None and len(active_obj.transforms_list) > 0

def is_dotnet_installed():
    try:
        dotnet_path = shutil.which("dotnet")
        if dotnet_path is None:
            print(
                "The 'dotnet' command was not found. Please ensure .NET is installed and the PATH environment variable is set correctly."
            )
            return False

        result = subprocess.run(
            [dotnet_path, "--list-runtimes"], capture_output=True, text=True
        )
        if result.returncode != 0:
            return False

        for line in result.stdout.splitlines():
            if "Microsoft.NETCore.App 9" in line:
                return True
        return False
    except Exception as e:
        print(f"Error checking .NET installation: {e}")
        traceback.print_exc()
        return False


def is_pythonnet_loaded():
    return importlib.util.find_spec("pythonnet") is not None