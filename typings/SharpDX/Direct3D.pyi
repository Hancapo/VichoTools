from __future__ import annotations
from enum import IntEnum, IntFlag
from typing import Any, Callable, ClassVar, Generic, TypeVar, overload
import SharpDX

T = TypeVar("T")

class Blob(SharpDX.ComObject):
    BufferPointer: Any
    BufferSize: SharpDX.PointerSize
    Tag: Any
    NativePointer: Any
    IsDisposed: bool
    def __init__(self, nativePtr: Any) -> None: ...
    def Dispose(self) -> None: ...
    def Equals(self, obj: Any) -> bool: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    @overload
    def QueryInterface(self, guid: Any, outPtr: Any) -> None: ...
    @overload
    def QueryInterface(self) -> T: ...
    @overload
    def QueryInterfaceOrNull(self, guid: Any) -> Any: ...
    @overload
    def QueryInterfaceOrNull(self) -> T: ...
    def ToString(self) -> str: ...

class CommonGuid:
    DebugObjectName: ClassVar[Any]
    def __init__(self) -> None: ...
    def Equals(self, obj: Any) -> bool: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    def ToString(self) -> str: ...

class DestructionNotifier:
    ...

class DeviceMultithread(SharpDX.ComObject):
    Tag: Any
    NativePointer: Any
    IsDisposed: bool
    def __init__(self, nativePtr: Any) -> None: ...
    def Dispose(self) -> None: ...
    def Enter(self) -> None: ...
    def Equals(self, obj: Any) -> bool: ...
    def GetHashCode(self) -> int: ...
    def GetMultithreadProtected(self) -> SharpDX.Mathematics.Interop.RawBool: ...
    def GetType(self) -> Any: ...
    def Leave(self) -> None: ...
    @overload
    def QueryInterface(self, guid: Any, outPtr: Any) -> None: ...
    @overload
    def QueryInterface(self) -> T: ...
    @overload
    def QueryInterfaceOrNull(self, guid: Any) -> Any: ...
    @overload
    def QueryInterfaceOrNull(self) -> T: ...
    def SetMultithreadProtected(self, bMTProtect: SharpDX.Mathematics.Interop.RawBool) -> SharpDX.Mathematics.Interop.RawBool: ...
    def ToString(self) -> str: ...

class DriverType(IntEnum):
    Unknown = 0
    Hardware = 1
    Reference = 2
    Null = 3
    Software = 4
    Warp = 5

class FeatureLevel(IntEnum):
    Level_9_1 = 37120
    Level_9_2 = 37376
    Level_9_3 = 37632
    Level_10_0 = 40960
    Level_10_1 = 41216
    Level_11_0 = 45056
    Level_11_1 = 45312
    Level_12_0 = 49152
    Level_12_1 = 49408

class InterpolationMode(IntEnum):
    Undefined = 0
    Constant = 1
    Linear = 2
    LinearCentroid = 3
    LinearNoperspective = 4
    LinearNoperspectiveCentroid = 5
    LinearSample = 6
    LinearNoperspectiveSample = 7

class MinimumPrecision(IntEnum):
    MinimumPrecisionDefault = 0
    MinimumPrecisionFloat16 = 1
    MinimumPrecisionFloat28 = 2
    MinimumPrecisionReserved = 3
    MinimumPrecisionSInt16 = 4
    MinimumPrecisionUInt16 = 5
    MinimumPrecisionAny16 = 240
    MinimumPrecisionAny10 = 241

class PrimitiveTopology(IntEnum):
    Undefined = 0
    PointList = 1
    LineList = 2
    LineStrip = 3
    TriangleList = 4
    TriangleStrip = 5
    LineListWithAdjacency = 10
    LineStripWithAdjacency = 11
    TriangleListWithAdjacency = 12
    TriangleStripWithAdjacency = 13
    PatchListWith1ControlPoints = 33
    PatchListWith2ControlPoints = 34
    PatchListWith3ControlPoints = 35
    PatchListWith4ControlPoints = 36
    PatchListWith5ControlPoints = 37
    PatchListWith6ControlPoints = 38
    PatchListWith7ControlPoints = 39
    PatchListWith8ControlPoints = 40
    PatchListWith9ControlPoints = 41
    PatchListWith10ControlPoints = 42
    PatchListWith11ControlPoints = 43
    PatchListWith12ControlPoints = 44
    PatchListWith13ControlPoints = 45
    PatchListWith14ControlPoints = 46
    PatchListWith15ControlPoints = 47
    PatchListWith16ControlPoints = 48
    PatchListWith17ControlPoints = 49
    PatchListWith18ControlPoints = 50
    PatchListWith19ControlPoints = 51
    PatchListWith20ControlPoints = 52
    PatchListWith21ControlPoints = 53
    PatchListWith22ControlPoints = 54
    PatchListWith23ControlPoints = 55
    PatchListWith24ControlPoints = 56
    PatchListWith25ControlPoints = 57
    PatchListWith26ControlPoints = 58
    PatchListWith27ControlPoints = 59
    PatchListWith28ControlPoints = 60
    PatchListWith29ControlPoints = 61
    PatchListWith30ControlPoints = 62
    PatchListWith31ControlPoints = 63
    PatchListWith32ControlPoints = 64

class ShaderMacro:
    Name: str
    Definition: str
    def __init__(self, name: str, definition: Any) -> None: ...
    @overload
    def Equals(self, other: ShaderMacro) -> bool: ...
    @overload
    def Equals(self, obj: Any) -> bool: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    def ToString(self) -> str: ...

class ShaderResourceViewDimension(IntEnum):
    Unknown = 0
    Buffer = 1
    Texture1D = 2
    Texture1DArray = 3
    Texture2D = 4
    Texture2DArray = 5
    Texture2DMultisampled = 6
    Texture2DMultisampledArray = 7
    Texture3D = 8
    TextureCube = 9
    TextureCubeArray = 10
    ExtendedBuffer = 11
