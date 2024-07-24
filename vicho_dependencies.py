from pathlib import Path
import sys
import os
class DependenciesManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DependenciesManager, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.clr = None
        self.List = None
        self.GameFiles = None
        self.Utils = None
        self.ScratchImage = None
        self.TexHelper = None
        self.WIC_FLAGS = None
        self.DXGI_FORMAT = None
        self.TEX_COMPRESS_FLAGS = None
        self.DDS_FLAGS = None
        self.TEX_FILTER_FLAGS = None

    @property
    def available(self):
        return all([self.clr, self.List, self.GameFiles, self.Utils])
    
    def load_dependencies(self):
        try:
            print("Initializing dependencies...")
            p = Path(__file__).resolve().parent
            runtime_loc = p / 'ytd' / 'cw_py' / 'libs' / 'runtimeconfig.json'
            sys.path.append(str(p / 'ytd' / 'cw_py' / 'libs'))
            
            if runtime_loc.exists():
                import pythonnet
                pythonnet.load("coreclr", runtime_config=str(runtime_loc))
            else:
                return False

            import clr
            print("CLR correctly loaded")

            clr.AddReference('CodeWalker.Core')
            clr.AddReference("System.Collections")
            clr.AddReference("DirectXTexNet")
            print("References added correctly")

            from System.Collections.Generic import List
            import CodeWalker.GameFiles as GameFiles
            import CodeWalker.Utils as Utils
            import DirectXTexNet
            print("Modules imported correctly")

            self.clr = clr
            self.List = List
            self.GameFiles = GameFiles
            self.Utils = Utils
            self.ScratchImage = DirectXTexNet.ScratchImage
            self.TexHelper = DirectXTexNet.TexHelper
            self.WIC_FLAGS = DirectXTexNet.WIC_FLAGS
            self.DXGI_FORMAT = DirectXTexNet.DXGI_FORMAT
            self.TEX_COMPRESS_FLAGS = DirectXTexNet.TEX_COMPRESS_FLAGS
            self.DDS_FLAGS = DirectXTexNet.DDS_FLAGS
            self.TEX_FILTER_FLAGS = DirectXTexNet.TEX_FILTER_FLAGS

            print("Dependencies loaded correctly")
            print(f"dependencies.available: {self.available}")
            print(f"clr: {self.clr}")
            print(f"List: {self.List}")
            print(f"GameFiles: {self.GameFiles}")
            print(f"Utils: {self.Utils}")

            return True
        except Exception as e:
            print(f"Error detail: {e}")
            import traceback
            traceback.print_exc()
            return False

dependencies_manager = DependenciesManager()

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

def is_pythonnet_loaded():
    try:
        import pythonnet
        return True
    except ImportError:
        return False