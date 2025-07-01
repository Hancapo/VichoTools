import os
import bpy
import subprocess
import shutil
import traceback
import importlib.util
from typing import List


DOTNET_LINK = "https://builds.dotnet.microsoft.com/dotnet/Runtime/9.0.6/dotnet-runtime-9.0.6-win-x64.exe"


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
        self.File = None

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

        # SharpDX stuff
        self.Vector3 = None
        self.Vector4 = None

        # Ymap stuff
        self.YmapFile = None
        self.YmapEntityDef = None
        self.rage__eLodType = None
        self.rage__ePriorityLevel = None
        self.MloInstanceData = None
        self.MloArchetype = None
        self.CMloArchetypeDefData = None
        self.CEntityDef = None
        self.MetaHash = None
        self.JenkHash = None
        self.JenkIndex = None

    @property
    def ymap_list(self) -> List["YmapFile"]:
        """Returns the list of YMAPs in the scene as YmapFile objects"""
        scene = bpy.context.scene
        ymap_bytes_list: List[bytes] = scene.get("ymap_list", [])
        actual_ymap_list: List["YmapFile"] = []
        for ymap_bytes in ymap_bytes_list:
            ymap = self.YmapFile()
            ymap.Load(ymap_bytes)
            actual_ymap_list.append(ymap)
        return actual_ymap_list
    
    @property
    def ymap_list_bytes(self) -> List[bytes]:
        """Returns the list of YMAPs in the scene as bytes"""
        scene = bpy.context.scene
        ymap_bytes_list: List[bytes] = scene.get("ymap_list", [])
        return ymap_bytes_list
    
    @ymap_list.setter
    def ymap_list(self, value: List["YmapFile"]):
        scene = bpy.context.scene
        scene["ymap_list"] = value
    
    def add_ymap(self, ymap_path: str) -> bool:
        """Adds a YMAP to the scene as bytes"""
        scene = bpy.context.scene
        ymap_bytes: bytes = bytes(self.File.ReadAllBytes(ymap_path))
        ymap_bytes_list: List[bytes] = scene.get("ymap_list", [])
        try:
            ymap_list_bytes = list(ymap_bytes_list)
            ymap_list_bytes.append(ymap_bytes)
            scene["ymap_list"] = ymap_list_bytes
            return True
        except Exception as e:
            print(f"Error adding ymap: {e}")
            return False
        
    def remove_ymap(self, index: int) -> bool:
        """Removes a YMAP from the scene"""
        scene = bpy.context.scene
        ymap_bytes_list: List[bytes] = scene.get("ymap_list", [])
        try:
            ymap_bytes_list.pop(index)
            scene["ymap_list"] = ymap_bytes_list
            return True
        except Exception as e:
            print(f"Error removing ymap: {e}")
            return False

    def get_ymap(self, index: int) -> "YmapFile":
        """Returns the YmapFile object at the specified index"""
        return self.ymap_list[index]
    
    def get_ymap_bytes(self, index: int) -> bytes:
        """Returns the YmapFile bytes at the specified index"""
        return self.ymap_list_bytes[index]

    @property
    def available(self):
        return all(
            [
                self.clr,
                self.List,
                self.File,
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
                self.Vector3,
                self.Vector4,
                self.YmapFile,
                self.YmapEntityDef,
                self.rage__eLodType,
                self.rage__ePriorityLevel,
                self.MloInstanceData,
                self.MloArchetype,
                self.CMloArchetypeDefData,
                self.CEntityDef,
                self.MetaHash,
                self.JenkHash,
                self.JenkIndex,
            ]
        )

    def load_dependencies(self):
        try:
            p = os.path.dirname(__file__)
            runtime_loc = rf"{p}\libs\vichotools.json"
            libs_loc = rf"{p}\libs"
            os.environ["PATH"] = libs_loc + os.pathsep + os.environ["PATH"]
            if os.path.exists(runtime_loc):
                import pythonnet
                pythonnet.load("coreclr", runtime_config=runtime_loc)
            else:
                return False

            import clr

            print("CLR OK")

            clr.AddReference(rf"{libs_loc}\CodeWalker.Core.dll")
            clr.AddReference("System.Collections")
            clr.AddReference(rf"{libs_loc}\TeximpNet.dll")
            print("References added correctly")

            from System.Collections.Generic import List
            import CodeWalker.GameFiles as GameFiles
            from System.IO import File
            from CodeWalker.GameFiles import (
                YmapFile,
                YmapEntityDef,
                rage__eLodType,
                rage__ePriorityLevel,
                MloInstanceData,
                MloArchetype,
                CMloArchetypeDefData,
                CEntityDef,
                MetaHash,
                JenkHash,
                JenkIndex,
            )
            import CodeWalker.Utils as Utils
            from TeximpNet import Surface as Surface, ImageFilter as ImageFilter
            from TeximpNet.Compression import (
                Compressor,
                CompressionFormat,
                CompressionQuality,
                OutputFileFormat,
                MipmapFilter,
                RoundMode,
            )

            from SharpDX import Vector3, Vector4

            print("Modules OK")

            self.clr = clr

            self.GameFiles = GameFiles
            self.Utils = Utils

            self.Vector3 = Vector3
            self.Vector4 = Vector4

            self.YmapFile = YmapFile
            self.YmapEntityDef = YmapEntityDef
            self.rage__eLodType = rage__eLodType
            self.rage__ePriorityLevel = rage__ePriorityLevel
            self.MloInstanceData = MloInstanceData
            self.MloArchetype = MloArchetype
            self.CMloArchetypeDefData = CMloArchetypeDefData
            self.CEntityDef = CEntityDef
            self.MetaHash = MetaHash
            self.JenkHash = JenkHash
            self.JenkIndex = JenkIndex

            self.List = List
            self.File = File

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
