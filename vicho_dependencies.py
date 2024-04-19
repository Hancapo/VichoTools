from pathlib import Path
import sys


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
