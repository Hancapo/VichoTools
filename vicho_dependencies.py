from pathlib import Path
import sys
import os


def is_dotnet_installed():
    path_env = os.getenv('PATH')
    paths = path_env.split(os.pathsep)
    for path in paths:
        dotnet_path = os.path.join(path, 'dotnet')
        if os.path.isfile(dotnet_path) or os.path.isfile(dotnet_path + '.exe'):
            print('.NET is installed.')
            return True
    print('Error: .NET is not installed')
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
