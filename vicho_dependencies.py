import os
import subprocess
import shutil
import traceback
import importlib.util

dotnet_link = "https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-desktop-8.0.11-windows-x64-installer"

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

        # TeximpNet stuff
        self.Surface = None
        self.Compressor = None
        self.CompressionFormat = None
        self.CompressionQuality = None
        self.OutputFileFormat = None
        self.MipmapFilter = None
        self.ImageFilter = None
        self.RoundMode = None

        # CodeWalker stuff
        self.GameFiles = None
        self.Utils = None

    @property
    def available(self):
        return all(
            [
                self.clr,
                self.List,
                self.Surface,
                self.Compressor,
                self.CompressionFormat,
                self.CompressionQuality,
                self.OutputFileFormat,
                self.MipmapFilter,
                self.ImageFilter,
                self.RoundMode,
                self.GameFiles,
                self.Utils,
            ]
        )

    def load_dependencies(self):
        try:
            p = os.path.dirname(__file__)
            runtime_loc = fr"{p}\libs\vichotools.json"
            libs_loc = fr"{p}\libs"
            os.environ["PATH"] = libs_loc + os.pathsep + os.environ["PATH"]
            if os.path.exists(runtime_loc):
                import pythonnet
                pythonnet.load("coreclr", runtime_config=runtime_loc)
            else:
                return False

            import clr

            print("CLR OK")

            clr.AddReference(fr'{libs_loc}\CodeWalker.Core.dll')
            clr.AddReference("System.Collections")
            clr.AddReference(fr'{libs_loc}\TeximpNet.dll')
            print("References added correctly")

            from System.Collections.Generic import List
            import CodeWalker.GameFiles as GameFiles
            import CodeWalker.Utils as Utils
            from TeximpNet import Surface as Surface, ImageFilter as ImageFilter
            from TeximpNet.Compression import (
                Compressor,
                CompressionFormat,
                CompressionQuality,
                OutputFileFormat,
                MipmapFilter,
                RoundMode
            )

            print("Modules OK")

            self.clr = clr

            self.GameFiles = GameFiles
            self.Utils = Utils
            
            self.List = List

            self.Surface = Surface
            self.Compressor = Compressor
            self.CompressionFormat = CompressionFormat
            self.CompressionQuality = CompressionQuality
            self.OutputFileFormat = OutputFileFormat
            self.MipmapFilter = MipmapFilter
            self.ImageFilter = ImageFilter
            self.RoundMode = RoundMode

            print("Dependencies loaded OK")
            print(f"dependencies.available: {self.available}")
            print(f"clr: {self.clr}")
            print(f"GameFiles: {self.GameFiles}")
            print(f"List: {self.List}")
            print(f"Utils: {self.Utils}")
            print(f"Surface: {self.Surface}")
            print(f"Compressor: {self.Compressor}")

            return True
        except Exception as e:
            print(f"Error detail: {e}")
            import traceback

            traceback.print_exc()
            return False


dependencies_manager = DependenciesManager()


def is_dotnet_installed():
    try:
        # Find the dotnet executable in the system's PATH
        dotnet_path = shutil.which("dotnet")
        if dotnet_path is None:
            print("The 'dotnet' command was not found. Please ensure .NET is installed and the PATH environment variable is set correctly.")
            return False

        result = subprocess.run([dotnet_path, "--list-runtimes"], capture_output=True, text=True)
        if result.returncode != 0:
            return False

        for line in result.stdout.splitlines():
            if "Microsoft.NETCore.App 8" in line:
                return True
        return False
    except Exception as e:
        print(f"Error checking .NET installation: {e}")
        traceback.print_exc()
        return False


def is_pythonnet_loaded():
    return importlib.util.find_spec("pythonnet") is not None
