from pathlib import Path
import subprocess
import sys


def is_dotnet_installed():
    try:
        result = subprocess.run(['dotnet', '--version'], capture_output=True, text=True, check=True)
        print(f'Installed .NET version: {result.stdout}')
        return True
    except subprocess.CalledProcessError:
        print('Error: .NET is not installed')
        return False
    except FileNotFoundError:
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
        pythonnet_installed = True
        return pythonnet_installed
    except ImportError:
        return False
