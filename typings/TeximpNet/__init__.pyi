from __future__ import annotations
from enum import IntEnum, IntFlag
from typing import Any, ClassVar, TypeVar, overload
import TeximpNet

T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
TFrom = TypeVar("TFrom")
TTo = TypeVar("TTo")
V = TypeVar("V")

class BGRAQuad:
    B: int
    G: int
    R: int
    A: int
    def __init__(self, b: int, g: int, r: int, a: int) -> None: ...
    def Equals(self, obj: Any) -> bool: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    @overload
    def ToRGBA(self) -> RGBAQuad: ...
    @overload
    def ToRGBA(self, color: RGBAQuad) -> None: ...
    def ToString(self) -> str: ...

class ColorOrder:
    RedIndex: int
    GreenIndex: int
    BlueIndex: int
    AlphaIndex: int
    RedMask: int
    GreenMask: int
    BlueMask: int
    AlphaMask: int
    RedShift: int
    GreenShift: int
    BlueShift: int
    AlphaShift: int
    IsBGRAOrder: bool
    LE_BGRA_RED_MASK: ClassVar[int]
    LE_BGRA_GREEN_MASK: ClassVar[int]
    LE_BGRA_BLUE_MASK: ClassVar[int]
    LE_BGRA_ALPHA_MASK: ClassVar[int]
    LE_RGBA_RED_MASK: ClassVar[int]
    LE_RGBA_GREEN_MASK: ClassVar[int]
    LE_RGBA_BLUE_MASK: ClassVar[int]
    LE_RGBA_ALPHA_MASK: ClassVar[int]
    BE_BGRA_RED_MASK: ClassVar[int]
    BE_BGRA_GREEN_MASK: ClassVar[int]
    BE_BGRA_BLUE_MASK: ClassVar[int]
    BE_BGRA_ALPHA_MASK: ClassVar[int]
    BE_RGBA_RED_MASK: ClassVar[int]
    BE_RGBA_GREEN_MASK: ClassVar[int]
    BE_RGBA_BLUE_MASK: ClassVar[int]
    BE_RGBA_ALPHA_MASK: ClassVar[int]
    def __init__(self, isLittleEndian: bool) -> None: ...
    def Equals(self, obj: Any) -> bool: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    def ToString(self) -> str: ...

class ImageColorType(IntEnum):
    MinIsWhite = 0
    MinIsBlack = 1
    RGB = 2
    Palette = 3
    RGBA = 4
    CMYK = 5

class ImageConversion(IntEnum):
    To4Bits = 0
    To8Bits = 1
    To16Bits555 = 2
    To16Bits565 = 3
    To24Bits = 4
    To32Bits = 5
    ToGreyscale = 6
    ToFloat = 7
    ToUInt16 = 8
    ToRGBF = 9
    ToRGBAF = 10
    ToRGB16 = 11
    ToRGBA16 = 12

class ImageFilter(IntEnum):
    Box = 0
    Bicubic = 1
    Bilinear = 2
    Bspline = 3
    CatmullRom = 4
    Lanczos3 = 5

class ImageFormat(IntEnum):
    BMP = 0
    ICO = 1
    JPEG = 2
    JNG = 3
    KOALA = 4
    LBM = 5
    IFF = 5
    MNG = 6
    PBM = 7
    PBMRAW = 8
    PCD = 9
    PCX = 10
    PGM = 11
    PGMRAW = 12
    PNG = 13
    PPM = 14
    PPMRAW = 15
    RAS = 16
    TARGA = 17
    TIFF = 18
    WBMP = 19
    PSD = 20
    CUT = 21
    XBM = 22
    XPM = 23
    DDS = 24
    GIF = 25
    HDR = 26
    FAXG3 = 27
    SGI = 28
    EXR = 29
    J2K = 30
    JP2 = 31
    PFM = 32
    PICT = 33
    RAW = 34
    WEBP = 35
    JXR = 36
    Unknown = -1

class ImageHelper:
    @overload
    @staticmethod
    def CalculateMipmapLevelDimensions(mipLevel: int, width: int, height: int) -> None: ...
    @overload
    @staticmethod
    def CalculateMipmapLevelDimensions(mipLevel: int, width: int, height: int, depth: int) -> None: ...
    @overload
    @staticmethod
    def ComputePitch(format: TeximpNet.DDS.DXGIFormat, width: int, height: int, rowPitch: int, slicePitch: int, widthCount: int, heightCount: int, legacyDword: bool = ...) -> None: ...
    @overload
    @staticmethod
    def ComputePitch(format: TeximpNet.DDS.DXGIFormat, width: int, height: int, rowPitch: int, slicePitch: int, widthCount: int, heightCount: int, bytesPerPixel: int, legacyDword: bool = ...) -> None: ...
    @overload
    @staticmethod
    def CopyColorImageData(dstPtr: Any, dstRowPitch: int, dstSlicePitch: int, srcPtr: Any, srcRowPitch: int, srcSlicePitch: int, width: int, height: int, depth: int, swizzle: bool = ...) -> None: ...
    @overload
    @staticmethod
    def CopyColorImageData(dstPtr: Any, srcPtr: Any, srcRowPitch: int, srcSlicePitch: int, width: int, height: int, depth: int, swizzle: bool = ...) -> None: ...
    @staticmethod
    def CopyImageData(dstPtr: Any, dstRowPitch: int, dstSlicePitch: int, srcPtr: Any, srcRowPitch: int, srcSlicePitch: int, width: int, height: int, depth: int) -> None: ...
    @staticmethod
    def CopyRGBALine(dstPtr: Any, srcPtr: Any, width: int, swizzle: bool = ...) -> None: ...
    @staticmethod
    def CountMipmaps(width: int, height: int, depth: int) -> int: ...
    @staticmethod
    def EnsureOneOrGreater(val: int) -> int: ...
    def Equals(self, obj: Any) -> bool: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    @staticmethod
    def NearestPowerOfTwo(v: int) -> int: ...
    @staticmethod
    def NextPowerOfTwo(v: int) -> int: ...
    @staticmethod
    def PreviousPowerOfTwo(v: int) -> int: ...
    def ToString(self) -> str: ...

class ImageLoadFlags(IntFlag):
    Default = 0
    TIFF_CMYK = 1
    TARGA_LoadRGB888 = 1
    RAW_Preview = 1
    PNG_IgnoreGamma = 1
    PSD_CMYK = 1
    PCD_Base = 1
    JPEG_Fast = 1
    ICO_MakeAlpha = 1
    GIF_Load256 = 1
    JPEG_Accurate = 2
    PCD_BaseDiv4 = 2
    RAW_Display = 2
    GIF_Playback = 2
    PSD_Lab = 2
    PCD_BaseDiv16 = 3
    JPEG_CMYK = 4
    JPEG_ExifRotate = 8
    JPEG_Greyscale = 16

class ImageSaveFlags(IntFlag):
    Default = 0
    BMP_SaveRLE = 1
    EXR_Float = 1
    PNM_SaveAscii = 1
    PNG_Z_BestSpeed = 1
    TARGA_SaveRLE = 2
    EXR_None = 2
    RAW_HalfSize = 4
    EXR_Zip = 4
    PNG_Z_DefaultCompression = 6
    EXR_Piz = 8
    RAW_Unprocessed = 8
    PNG_Z_BestCompression = 9
    EXR_PXR24 = 16
    EXR_B44 = 32
    EXR_LC = 64
    JXR_Lossless = 100
    JPEG_QualitySuperb = 128
    TIFF_PackBits = 256
    PNG_Z_NoCompression = 256
    JPEG_QualityGood = 256
    WEBP_Lossless = 256
    PNG_Interlaced = 512
    TIFF_Deflate = 512
    JPEG_QualityNormal = 512
    JPEG_QualityAverage = 1024
    TIFF_AdobeDeflate = 1024
    TIFF_None = 2048
    JPEG_QualityBad = 2048
    TIFF_CCITTFAX3 = 4096
    JPEG_Subsampling_411 = 4096
    TIFF_CCITTFAX4 = 8192
    JXR_Progressive = 8192
    JPEG_Progressive = 8192
    JPEG_Subsampling_420 = 16384
    TIFF_LZW = 16384
    JPEG_Subsampling_422 = 32768
    TIFF_JPEG = 32768
    JPEG_Subsampling_444 = 65536
    TIFF_LogLuv = 65536
    JPEG_Optimize = 131072
    JPEG_Baseline = 262144

class ImageType(IntEnum):
    Unknown = 0
    Bitmap = 1
    UInt16 = 2
    Int16 = 3
    UInt32 = 4
    Int32 = 5
    Float = 6
    Double = 7
    Complex = 8
    RGB16 = 9
    RGBA16 = 10
    RGBF = 11
    RGBAF = 12

class MemoryHelper:
    @staticmethod
    def AddIntPtr(ptr: Any, offset: int) -> Any: ...
    @staticmethod
    def AllocateClearedMemory(sizeInBytes: int, clearValue: int = ..., alignment: int = ...) -> Any: ...
    @staticmethod
    def AllocateMemory(sizeInBytes: int, alignment: int = ...) -> Any: ...
    @staticmethod
    def As(src: TFrom) -> TTo: ...
    @staticmethod
    def AsPointer(src: T) -> Any: ...
    @staticmethod
    def AsPointerReadonly(src: T) -> Any: ...
    @staticmethod
    def AsReadonly(src: TFrom) -> TTo: ...
    @staticmethod
    def AsRef(pSrc: Any) -> T: ...
    @staticmethod
    def CastToEnum(value: V) -> T: ...
    @staticmethod
    def ClearMemory(memoryPtr: Any, clearValue: int, sizeInBytesToClear: int) -> None: ...
    @staticmethod
    def Compare(firstData: list[int], secondData: list[int]) -> bool: ...
    @staticmethod
    def ComputeFNVModifiedHashCode(data: list[int]) -> int: ...
    @overload
    @staticmethod
    def CopyBytes(srcArray: list[int], srcStartIndex: int, destArray: list[T], destStartIndex: int, count: int) -> None: ...
    @overload
    @staticmethod
    def CopyBytes(srcArray: list[T], srcStartIndex: int, destArray: list[int], destStartIndex: int, count: int) -> None: ...
    @staticmethod
    def CopyMemory(pDest: Any, pSrc: Any, sizeInBytesToCopy: int) -> None: ...
    @staticmethod
    def Count(source: list[T]) -> int: ...
    @staticmethod
    def DisposeCollection(collection: Any) -> None: ...
    def Equals(self, obj: Any) -> bool: ...
    @staticmethod
    def FreeMemory(memoryPtr: Any) -> None: ...
    @staticmethod
    def FromByteArray(source: list[int]) -> list[T]: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    @staticmethod
    def IsMemoryAligned(memoryPtr: Any, alignment: int = ...) -> bool: ...
    @staticmethod
    def PinObject(obj: Any) -> Any: ...
    @overload
    @staticmethod
    def Read(pSrc: Any, data: list[T], startIndexInArray: int, count: int) -> None: ...
    @overload
    @staticmethod
    def Read(pSrc: Any) -> T: ...
    @overload
    @staticmethod
    def Read(pSrc: Any, value: T) -> None: ...
    @staticmethod
    def ReadStreamFully(stream: Any, initialLength: int) -> list[int]: ...
    @overload
    @staticmethod
    def SizeOf() -> int: ...
    @overload
    @staticmethod
    def SizeOf(array: list[T]) -> int: ...
    @staticmethod
    def Swap(left: T, right: T) -> None: ...
    @staticmethod
    def ToByteArray(source: list[T]) -> list[int]: ...
    def ToString(self) -> str: ...
    @staticmethod
    def UnpinObject(obj: Any) -> None: ...
    @overload
    @staticmethod
    def Write(pDest: Any, data: list[T], startIndexInArray: int, count: int) -> None: ...
    @overload
    @staticmethod
    def Write(pDest: Any, data: T) -> None: ...

class RGBAQuad:
    R: int
    G: int
    B: int
    A: int
    def __init__(self, r: int, g: int, b: int, a: int) -> None: ...
    def Equals(self, obj: Any) -> bool: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    @overload
    def ToBGRA(self) -> BGRAQuad: ...
    @overload
    def ToBGRA(self, color: BGRAQuad) -> None: ...
    def ToString(self) -> str: ...

class StreamTransferBuffer:
    Pointer: Any
    ByteArray: list[int]
    Length: int
    LastReadByteCount: int
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, numBytes: int, avoidLOH: bool = ...) -> None: ...
    def Dispose(self) -> None: ...
    def Equals(self, obj: Any) -> bool: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Any: ...
    @overload
    def Read(self, input: Any, value: T) -> bool: ...
    @overload
    def Read(self, input: Any) -> T: ...
    def ReadBytes(self, input: Any, numBytes: int) -> int: ...
    def Resize(self, numBytes: int, avoidLOH: bool = ...) -> None: ...
    def ToString(self) -> str: ...
    def Write(self, output: Any, value: T) -> None: ...
    def WriteBytes(self, output: Any, numBytes: int) -> None: ...

class Surface:
    IsLittleEndian: ClassVar[bool]
    IsBGRAOrder: ClassVar[bool]
    ColorOrder: ClassVar[ColorOrder]
    IsDisposed: bool
    ImageType: ImageType
    BitsPerPixel: int
    Pitch: int
    Width: int
    Height: int
    RedMask: int
    GreenMask: int
    BlueMask: int
    IsTransparent: bool
    ColorType: ImageColorType
    DataPtr: Any
    PalettePtr: Any
    HasPalette: bool
    PaletteColorCount: int
    NativePtr: Any
    @overload
    def __init__(self, width: int, height: int) -> None: ...
    @overload
    def __init__(self, width: int, height: int, hasAlpha: bool) -> None: ...
    @overload
    def __init__(self, bpp: int, width: int, height: int) -> None: ...
    @overload
    def __init__(self, bpp: int, width: int, height: int, redMask: int, greenMask: int, blueMask: int) -> None: ...
    @overload
    def __init__(self, imageType: ImageType, bpp: int, width: int, height: int) -> None: ...
    @overload
    def __init__(self, imageType: ImageType, bpp: int, width: int, height: int, redMask: int, greenMask: int, blueMask: int) -> None: ...
    @overload
    def __init__(self, imagePtr: Any) -> None: ...
    def AdjustBrightness(self, percentage: float) -> bool: ...
    def AdjustContrast(self, percentage: float) -> bool: ...
    def AdjustGamma(self, gamma: float) -> bool: ...
    @overload
    def Clone(self) -> Surface: ...
    @overload
    def Clone(self, left: int, top: int, right: int, bottom: int) -> Surface: ...
    def ConvertTo(self, convertTo: ImageConversion) -> bool: ...
    def CopyFrom(self, src: Surface, left: int, top: int, alphaBlend: int = ...) -> bool: ...
    def Dispose(self) -> None: ...
    def Equals(self, obj: Any) -> bool: ...
    def FlipHorizontally(self) -> bool: ...
    def FlipVertically(self) -> bool: ...
    def GenerateMipMaps(self, mipChain: Any, filter: ImageFilter, includeFirst: bool = ..., maxLevel: int = ...) -> bool: ...
    def GetHashCode(self) -> int: ...
    def GetScanLine(self, scanLine: int) -> Any: ...
    def GetType(self) -> Any: ...
    def Invert(self) -> bool: ...
    @overload
    @staticmethod
    def LoadFromFile(filename: str, flags: ImageLoadFlags = ...) -> Surface: ...
    @overload
    @staticmethod
    def LoadFromFile(filename: str, flipImage: bool, flags: ImageLoadFlags = ...) -> Surface: ...
    @staticmethod
    def LoadFromRawData(imageDataPtr: Any, width: int, height: int, rowPitch: int, isBGRA: bool, isTopDown: bool = ...) -> Surface: ...
    @overload
    @staticmethod
    def LoadFromStream(stream: Any, flags: ImageLoadFlags = ...) -> Surface: ...
    @overload
    @staticmethod
    def LoadFromStream(stream: Any, flipImage: bool, flags: ImageLoadFlags = ...) -> Surface: ...
    def PreMultiplyAlpha(self) -> bool: ...
    def Resize(self, width: int, height: int, filter: ImageFilter) -> bool: ...
    def Rotate(self, angle: float) -> bool: ...
    def SaveToFile(self, format: ImageFormat, fileName: str, flags: ImageSaveFlags = ...) -> bool: ...
    def SaveToStream(self, format: ImageFormat, stream: Any, flags: ImageSaveFlags = ...) -> bool: ...
    def SwapColors(self, colorToReplace: RGBAQuad, colorToReplaceWith: RGBAQuad, ignoreAlpha: bool) -> bool: ...
    def ToString(self) -> str: ...

class TeximpException:
    TargetSite: Any
    Message: str
    Data: Any
    InnerException: Any
    HelpLink: str
    Source: str
    HResult: int
    StackTrace: str
    @overload
    def __init__(self, message: str) -> None: ...
    @overload
    def __init__(self, message: str, innerException: Any) -> None: ...
    def Equals(self, obj: Any) -> bool: ...
    def GetBaseException(self) -> Any: ...
    def GetHashCode(self) -> int: ...
    def GetObjectData(self, info: Any, context: Any) -> None: ...
    @overload
    def GetType(self) -> Any: ...
    @overload
    def GetType(self) -> Any: ...
    def ToString(self) -> str: ...