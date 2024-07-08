from pathlib import Path
import sys
import os

def is_dotnet_installed():
    path_env = os.getenv('PATH')
    dotnet_runtime_path = None
    for path in path_env.split(os.pathsep):
        if os.path.isdir(path) and 'dotnet' in path.lower():
            shared_path = os.path.join(path, 'shared', 'Microsoft.NETCore.App')
            if os.path.isdir(shared_path):
                dotnet_runtime_path = shared_path
                break
    if dotnet_runtime_path:
        for version in os.listdir(dotnet_runtime_path):
            if version.startswith("8."):
                coreclr_path = os.path.join(dotnet_runtime_path, version, 'coreclr.dll')
                if os.path.isfile(coreclr_path):
                    return True
    return False


def depen_installed():
    try:
        p = Path(__file__).resolve().parent
        runtime_loc = f'{p}/ytd/cw_py/libs/runtimeconfig.json'
        sys.path.append(f'{p}/ytd/cw_py/libs')
        if Path(runtime_loc).exists():
            from pythonnet import load
            load("coreclr", runtime_config=runtime_loc)
        import clr
        return True
    except ImportError:
        return False