import importlib
import os
import subprocess
import time
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
    return is_dotnet_runtime_installed(major=9)


_DOTNET_CHECK_CACHE = {
    "ts": 0.0,
    "major": None,
    "result": False,
    "dotnet_path": None,
}
_DOTNET_CHECK_TTL_SECONDS = 15.0


def _find_dotnet_executable() -> str | None:
    # Blender's environment may not inherit your user PATH, so try common locations too.
    candidates = []
    candidates.append(shutil.which("dotnet"))

    # Typical install locations.
    pf = os.environ.get("ProgramW6432") or os.environ.get("ProgramFiles")
    pfx86 = os.environ.get("ProgramFiles(x86)")
    local = os.environ.get("LOCALAPPDATA")

    if pf:
        candidates.append(os.path.join(pf, "dotnet", "dotnet.exe"))
    if pfx86:
        candidates.append(os.path.join(pfx86, "dotnet", "dotnet.exe"))
    if local:
        candidates.append(os.path.join(local, "Microsoft", "dotnet", "dotnet.exe"))

    for p in candidates:
        if p and os.path.exists(p):
            return p
    return None


def is_dotnet_runtime_installed(*, major: int) -> bool:
    try:
        now = time.monotonic()
        if (
            _DOTNET_CHECK_CACHE["major"] == major
            and (now - float(_DOTNET_CHECK_CACHE["ts"])) < _DOTNET_CHECK_TTL_SECONDS
        ):
            return bool(_DOTNET_CHECK_CACHE["result"])

        dotnet_path = _find_dotnet_executable()
        _DOTNET_CHECK_CACHE["ts"] = now
        _DOTNET_CHECK_CACHE["major"] = major
        _DOTNET_CHECK_CACHE["dotnet_path"] = dotnet_path

        if dotnet_path is None:
            _DOTNET_CHECK_CACHE["result"] = False
            return False

        create_no_window = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        result = subprocess.run(
            [dotnet_path, "--list-runtimes"],
            capture_output=True,
            text=True,
            creationflags=create_no_window,
        )
        if result.returncode != 0:
            _DOTNET_CHECK_CACHE["result"] = False
            return False

        target_prefix = f"Microsoft.NETCore.App {major}."
        ok = any(line.startswith(target_prefix) for line in result.stdout.splitlines())
        _DOTNET_CHECK_CACHE["result"] = ok
        return ok
    except Exception as e:
        print(f"Error checking .NET installation: {e}")
        traceback.print_exc()
        _DOTNET_CHECK_CACHE["result"] = False
        return False


def is_pythonnet_loaded():
    # find_spec can be false-negative in some Blender extension layouts; fall back to import.
    if importlib.util.find_spec("pythonnet") is not None:
        return True
    try:
        import pythonnet  # noqa: F401

        return True
    except Exception:
        return False
