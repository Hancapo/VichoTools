from __future__ import annotations

from typing import Any

import CodeWalker.GameFiles as GameFiles
import CodeWalker.Utils as Utils
import TeximpNet as TeximpNet
import TeximpNet.Compression as TeximpNetCompression
import SharpDX as SharpDX
import KeepA as KeepA

class DependenciesManager:
    clr: Any
    List: Any
    File: Any
    Enum: Any
    UInt32: Any

    Surface: type[TeximpNet.Surface]
    Compressor: type[TeximpNetCompression.Compressor]
    CompressionFormat: type[TeximpNetCompression.CompressionFormat]
    CompressionQuality: type[TeximpNetCompression.CompressionQuality]
    OutputFileFormat: type[TeximpNetCompression.OutputFileFormat]
    MipmapFilter: type[TeximpNetCompression.MipmapFilter]
    ImageFilter: type[TeximpNet.ImageFilter]
    RoundMode: type[TeximpNetCompression.RoundMode]

    GameFiles: GameFiles
    Utils: Utils

    Vector3: type[SharpDX.Vector3]
    Vector4: type[SharpDX.Vector4]

    YmapFile: type[GameFiles.YmapFile]
    YmapEntityDef: type[GameFiles.YmapEntityDef]
    rage__eLodType: type[GameFiles.rage__eLodType]
    rage__ePriorityLevel: type[GameFiles.rage__ePriorityLevel]
    MloInstanceData: type[GameFiles.MloInstanceData]
    MloArchetype: type[GameFiles.MloArchetype]
    CMloInstanceDef: type[GameFiles.CMloInstanceDef]
    CMloArchetypeDefData: type[GameFiles.CMloArchetypeDefData]
    CEntityDef: type[GameFiles.CEntityDef]
    MetaHash: type[GameFiles.MetaHash]
    JenkHash: type[GameFiles.JenkHash]
    JenkIndex: type[GameFiles.JenkIndex]
    CMapData: type[GameFiles.CMapData]
    BoxOccluder: type[GameFiles.BoxOccluder]
    YmapBoxOccluder: type[GameFiles.YmapBoxOccluder]
    OccludeModel: type[GameFiles.OccludeModel]
    YmapOccludeModel: type[GameFiles.YmapOccludeModel]
    FlagsUint: type[GameFiles.FlagsUint]
    YmapOccludeModelTriangle: type[GameFiles.YmapOccludeModelTriangle]

    FolderBrowser: type[KeepA.FolderBrowser]

    def load_dependencies(self) -> bool: ...
    @property
    def available(self) -> bool: ...

dependencies_manager: DependenciesManager
