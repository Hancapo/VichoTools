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
        self.File = None
        self.Enum = None
        self.UInt32 = None
        self.Action = None
        self.Task = None
        self.CollectTextures = None
        self.WriteTexturesAsync = None
        self.HashSet = None
        self.String = None

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
        self.GTA5Keys = None
        self.GameFileCache = None

        # SharpDX stuff
        self.Vector3 = None
        self.Vector4 = None
        self.Quaternion = None

        # Ymap stuff
        self.YmapFile = None
        self.YmapEntityDef = None
        self.rage__eLodType = None
        self.rage__ePriorityLevel = None
        self.MloInstanceData = None
        self.MloArchetype = None
        self.CMloInstanceDef = None
        self.CMloArchetypeDefData = None
        self.CEntityDef = None
        self.MetaHash = None
        self.JenkHash = None
        self.JenkIndex = None
        self.CMapData = None

        self.BoxOccluder = None
        self.YmapBoxOccluder = None
        self.OccludeModel = None
        self.YmapOccludeModel = None
        self.FlagsUint = None
        self.YmapOccludeModelTriangle = None
        
        # KeepA stuff
        self.FolderBrowser = None

        self.gamecache = None

    @property
    def gamecache(self):
        return self._gamecache
    
    @gamecache.setter
    def gamecache(self, value):
        self._gamecache = value

    @property
    def available(self):
        return all(
            [
                self.clr,
                self.List,
                self.File,
                self.Enum,
                self.UInt32,
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
                self.Quaternion,
                self.YmapFile,
                self.YmapEntityDef,
                self.rage__eLodType,
                self.rage__ePriorityLevel,
                self.MloInstanceData,
                self.MloArchetype,
                self.CMloInstanceDef,
                self.CMloArchetypeDefData,
                self.CEntityDef,
                self.MetaHash,
                self.JenkHash,
                self.JenkIndex,
                self.CMapData,
                self.FolderBrowser,
                self.BoxOccluder,
                self.YmapBoxOccluder,
                self.OccludeModel,
                self.YmapOccludeModel,
                self.FlagsUint,
                self.YmapOccludeModelTriangle,
                self.Action,
                self.Task,
                self.HashSet,
                self.String,
                self.CollectTextures,
                self.WriteTexturesAsync,
                self.GTA5Keys,
                self.GameFileCache,
            ]
        )

    def load_dependencies(self):
        try:
            p = os.path.dirname(__file__)
            runtime_loc_net10 = rf"{p}\libs\vichotools.json"
            runtime_loc_net9 = rf"{p}\libs\vichotools.net9.json"
            libs_loc = rf"{p}\libs"
            os.environ["PATH"] = libs_loc + os.pathsep + os.environ["PATH"]
            if os.path.exists(runtime_loc_net10):
                import pythonnet
                try:
                    pythonnet.load("coreclr", runtime_config=runtime_loc_net10)
                except Exception:
                    # Fallback for machines that only have .NET 9 installed.
                    if os.path.exists(runtime_loc_net9):
                        pythonnet.load("coreclr", runtime_config=runtime_loc_net9)
                    else:
                        raise
            else:
                return False

            import clr

            print("CLR OK")

            clr.AddReference(rf"{libs_loc}\CodeWalker.Core.dll")
            clr.AddReference("System.Collections")
            clr.AddReference(rf"{libs_loc}\TeximpNet.dll")
            clr.AddReference(rf"{libs_loc}\KeepA.dll")
            print("References added correctly")

            from System.Collections.Generic import List, HashSet
            from System import Enum, UInt32, Action, String
            from System.Threading.Tasks import Task
            import CodeWalker.GameFiles as GameFiles
            from System.IO import File
            from CodeWalker.GameFiles import (
                YmapFile,
                YmapEntityDef,
                rage__eLodType,
                rage__ePriorityLevel,
                MloInstanceData,
                MloArchetype,
                CMloInstanceDef,
                CMloArchetypeDefData,
                CEntityDef,
                MetaHash,
                JenkHash,
                JenkIndex,
                CMapData,
                BoxOccluder,
                YmapBoxOccluder,
                OccludeModel,
                YmapOccludeModel,
                FlagsUint,
                YmapOccludeModelTriangle
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

            from SharpDX import Vector3, Vector4, Quaternion
            from KeepA import FolderBrowser

            print("Modules OK")

            self.clr = clr

            self.GameFiles = GameFiles
            self.Utils = Utils
            self.Enum = Enum
            self.UInt32 = UInt32

            self.Vector3 = Vector3
            self.Vector4 = Vector4
            self.Quaternion = Quaternion

            self.YmapFile = YmapFile
            self.YmapEntityDef = YmapEntityDef
            self.rage__eLodType = rage__eLodType
            self.rage__ePriorityLevel = rage__ePriorityLevel
            self.MloInstanceData = MloInstanceData
            self.MloArchetype = MloArchetype
            self.CMloInstanceDef = CMloInstanceDef
            self.CMloArchetypeDefData = CMloArchetypeDefData
            self.CEntityDef = CEntityDef
            self.MetaHash = MetaHash
            self.JenkHash = JenkHash
            self.JenkIndex = JenkIndex
            self.CMapData = CMapData

            self.BoxOccluder = BoxOccluder
            self.YmapBoxOccluder = YmapBoxOccluder
            self.FlagsUint = FlagsUint
            self.OccludeModel = OccludeModel
            self.YmapOccludeModel = YmapOccludeModel
            self.YmapOccludeModelTriangle = YmapOccludeModelTriangle

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
            
            self.FolderBrowser = FolderBrowser

            print("Dependencies loaded OK")
            print(f"dependencies.available: {self.available}")
            print(f"clr: {self.clr}")
            print(f"GameFiles: {self.GameFiles}")
            print(f"List: {self.List}")
            print(f"Utils: {self.Utils}")
            print(f"Surface: {self.Surface}")
            print(f"Compressor: {self.Compressor}")
            print(f"YmapOccludeModel: {self.YmapBoxOccluder}")

            return True
        except Exception as e:
            print(f"Error detail: {e}")
            import traceback

            traceback.print_exc()
            return False


dependencies_manager = DependenciesManager()
