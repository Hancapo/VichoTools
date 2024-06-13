from pathlib import Path
import sys
import os


def is_dotnet_installed():
    path_env = os.getenv('PATH')
    dotnet_sdk_path = None
    for path in path_env.split(os.pathsep):
        if os.path.isdir(path) and 'dotnet' in path.lower():
            sdk_path = os.path.join(path, 'sdk')
            if os.path.isdir(sdk_path):
                dotnet_sdk_path = sdk_path
                break
    if dotnet_sdk_path:
        for version in os.listdir(dotnet_sdk_path):
            if version.startswith("8."):
                dotnet_dll_path = os.path.join(dotnet_sdk_path, version, 'dotnet.dll')
                if os.path.isfile(dotnet_dll_path):
                    print(f".NET SDK version 8 found: {dotnet_dll_path}")
                    return True
    else:
        print("No .NET SDK found in PATH.")
    
    print("Please install .NET SDK 8.0 or later from https://dotnet.microsoft.com/download/dotnet/5.0")
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