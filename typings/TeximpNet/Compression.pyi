from __future__ import annotations
from enum import IntEnum, IntFlag
from typing import Any, ClassVar, Generic, TypeVar, overload
import TeximpNet

T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")

class AlphaMode(IntEnum):
    None_ = 0
    Transparency = 1
    Premultiplied = 2

class CompressionFormat(IntEnum):
    BGRA = 0
    DXT1 = 1
    BC1 = 1
    DXT1a = 2
    BC1a = 2
    DXT3 = 3
    BC2 = 3
    DXT5 = 4
    BC3 = 4
    DXT5n = 5
    BC3n = 5
    BC4 = 6
    BC5 = 7
    BC6 = 10
    BC7 = 11
    BC3_RGBM = 12
    ETC1 = 13
    ETC2_R = 14
    ETC2_RG = 15
    ETC2_RGB = 16
    ETC2_RGBA = 17
    ETC2_RGB_A1 = 18
    ETC2_RGBM = 19
    PVR_2BPP_RGB = 20
    PVR_4BPP_RGB = 21
    PVR_2BPP_RGBA = 22
    PVR_4BPP_RGBA = 23

class CompressionQuality(IntEnum):
    Fastest = 0
    Normal = 1
    Production = 2
    Highest = 3

class Compressor:
    NativePtr: Any
    IsDisposed: bool
    Input: Compressor.InputOptions
    Compression: Compressor.CompressionOptions
    Output: Compressor.OutputOptions
    HasLastError: bool
    LastError: CompressorError
    LastErrorString: str
    def __init__(self) -> None: ...
    def Dispose(self) -> None: ...
    def Equals(self, obj: Any) -> bool: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    @overload
    def Process(self, outputFileName: str) -> bool: ...
    @overload
    def Process(self, stream: Any) -> bool: ...
    @overload
    def Process(self, compressedImages: TeximpNet.DDS.DDSContainer) -> bool: ...
    def ToString(self) -> str: ...

    class CompressionOptions:
        NativePtr: Any
        Format: CompressionFormat
        Quality: CompressionQuality
        def Equals(self, obj: Any) -> bool: ...
        def GetColorWeights(self, red_weight: float, green_weight: float, blue_weight: float, alpha_weight: float) -> None: ...
        def GetHashCode(self) -> int: ...
        def GetPixelFormat(self, bitsPerPixel: int, red_mask: int, green_mask: int, blue_mask: int, alpha_mask: int) -> None: ...
        def GetQuantization(self, enableColorDithering: bool, enableAlphaDithering: bool, binaryAlpha: bool, alphaThreshold: int) -> None: ...
        def GetType(self) -> Any: ...
        def SetBGRAPixelFormat(self) -> None: ...
        def SetColorWeights(self, red_weight: float, green_weight: float, blue_weight: float, alpha_weight: float) -> None: ...
        def SetPixelFormat(self, bitsPerPixel: int, red_mask: int, green_mask: int, blue_mask: int, alpha_mask: int) -> None: ...
        def SetQuantization(self, enableColorDithering: bool, enableAlphaDithering: bool, binaryAlpha: bool, alphaThreshold: int = ...) -> None: ...
        def SetRGBAPixelFormat(self) -> None: ...
        def ToString(self) -> str: ...

    class InputOptions:
        NativePtr: Any
        TextureType: TextureType
        Width: int
        Height: int
        Depth: int
        FaceCount: int
        MipmapCount: int
        GenerateMipmaps: bool
        AlphaMode: AlphaMode
        RoundMode: RoundMode
        MaxTextureExtent: int
        MipmapFilter: MipmapFilter
        WrapMode: WrapMode
        IsNormalMap: bool
        NormalizeMipmaps: bool
        ConvertToNormalMap: bool
        HasData: bool
        def ClearTextureLayout(self) -> None: ...
        def Equals(self, obj: Any) -> bool: ...
        def GetGamma(self, inputGamma: float, outputGamma: float) -> None: ...
        def GetHashCode(self) -> int: ...
        def GetHeightEvaluation(self, redScale: float, greenScale: float, blueScale: float, alphaScale: float) -> None: ...
        def GetKaiserParameters(self, width: float, alpha: float, stretch: float) -> None: ...
        def GetNormalFilter(self, small: float, medium: float, big: float, large: float) -> None: ...
        def GetType(self) -> Any: ...
        @overload
        def SetData(self, data: TeximpNet.Surface) -> bool: ...
        @overload
        def SetData(self, cubeFaces: list[TeximpNet.Surface]) -> bool: ...
        @overload
        def SetData(self, data: TeximpNet.DDS.MipData, isBGRA: bool) -> bool: ...
        @overload
        def SetData(self, cubeFaces: list[TeximpNet.DDS.MipData], isBGRA: bool) -> bool: ...
        def SetGamma(self, inputGamma: float, outputGamma: float) -> None: ...
        def SetHeightEvaluation(self, redScale: float, greenScale: float, blueScale: float, alphaScale: float) -> None: ...
        def SetKaiserParameters(self, width: float = ..., alpha: float = ..., stretch: float = ...) -> None: ...
        @overload
        def SetMipmapData(self, data: Any, isBGRA: bool, imageInfo: ImageInfo) -> bool: ...
        @overload
        def SetMipmapData(self, data: TeximpNet.Surface, mipmapLevel: int = ..., arrayIndex: int = ...) -> bool: ...
        @overload
        def SetMipmapData(self, data: TeximpNet.Surface, face: CubeMapFace, mipmapLevel: int = ...) -> bool: ...
        @overload
        def SetMipmapData(self, data: TeximpNet.DDS.MipData, isBGRA: bool, mipLevel: int = ..., arrayIndex: int = ...) -> bool: ...
        @overload
        def SetMipmapData(self, data: TeximpNet.DDS.MipData, isBGRA: bool, face: CubeMapFace, mipmapLevel: int = ...) -> bool: ...
        def SetMipmapGeneration(self, generateMips: bool, maxLevel: int = ...) -> None: ...
        def SetNormalFilter(self, small: float, medium: float, big: float, large: float) -> None: ...
        def SetTextureLayout(self, type: TextureType, width: int, height: int, depth: int = ..., arrayCount: int = ...) -> None: ...
        def ToString(self) -> str: ...

    class OutputOptions:
        NativePtr: Any
        OutputHeader: bool
        IsSRGBColorSpace: bool
        OutputFileFormat: OutputFileFormat
        def Equals(self, obj: Any) -> bool: ...
        def GetHashCode(self) -> int: ...
        def GetType(self) -> Any: ...
        def ToString(self) -> str: ...

class CompressorError(IntEnum):
    Unknown = 0
    InvalidInput = 1
    UnsupportedFeature = 2
    CudaError = 3
    FileOpen = 4
    FileWrite = 5
    UnsupportedOutputFormat = 6

class CubeMapFace(IntEnum):
    Positive_X = 0
    Negative_X = 1
    Positive_Y = 2
    Negative_Y = 3
    Positive_Z = 4
    Negative_Z = 5
    None_ = -1

class ImageInfo:
    Width: int
    Height: int
    Depth: int
    ArrayIndex: int
    MipLevel: int
    RowPitch: int
    SlicePitch: int
    def __init__(self, width: int, height: int, depth: int, arrayIndex: int, mipLevel: int, rowPitch: int, slicePitch: int) -> None: ...
    def Equals(self, obj: Any) -> bool: ...
    @overload
    @staticmethod
    def From2D(width: int, height: int, mipLevel: int = ..., arrayIndex: int = ...) -> ImageInfo: ...
    @overload
    @staticmethod
    def From2D(width: int, height: int, rowPitch: int, mipLevel: int = ..., arrayIndex: int = ...) -> ImageInfo: ...
    @overload
    @staticmethod
    def From3D(width: int, height: int, depth: int, mipLevel: int = ...) -> ImageInfo: ...
    @overload
    @staticmethod
    def From3D(width: int, height: int, depth: int, rowPitch: int, slicePitch: int, mipLevel: int = ...) -> ImageInfo: ...
    @overload
    @staticmethod
    def FromCube(size: int, face: CubeMapFace, mipLevel: int = ...) -> ImageInfo: ...
    @overload
    @staticmethod
    def FromCube(size: int, face: CubeMapFace, rowPitch: int, mipLevel: int = ...) -> ImageInfo: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    def ToString(self) -> str: ...

class InputFormat(IntEnum):
    BGRA_8UB = 0
    RGBA_16F = 1
    RGBA_32F = 2
    R_32F = 3

class MipmapFilter(IntEnum):
    Box = 0
    Triangle = 1
    Kaiser = 2

class OutputFileFormat(IntEnum):
    DDS = 0
    DDS10 = 1
    KTX = 2

class RoundMode(IntEnum):
    None_ = 0
    ToNextPowerOfTwo = 1
    ToNearestPowerOfTwo = 2
    ToPreviousPowerOfTwo = 3
    ToNextMultipleOfFour = 4
    ToNearestMultipleOfFour = 5
    ToPreviousMultipleOfFour = 6

class TextureType(IntEnum):
    Texture2D = 0
    TextureCube = 1
    Texture3D = 2
    Texture2DArray = 3

class WrapMode(IntEnum):
    Clamp = 0
    Repeat = 1
    Mirror = 2
