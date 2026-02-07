from __future__ import annotations
from enum import IntEnum, IntFlag
from typing import Any, Callable, ClassVar, Generic, TypeVar, overload
import CodeWalker

class DDSIO:
    def Equals(self, obj: Any) -> bool: ...
    @staticmethod
    def GetDDSFile(texture: CodeWalker.GameFiles.Texture) -> list[int]: ...
    @staticmethod
    def GetDXGIFormat(f: CodeWalker.GameFiles.TextureFormat) -> DDSIO.DXGI_FORMAT: ...
    def GetHashCode(self) -> int: ...
    @staticmethod
    def GetPixels(texture: CodeWalker.GameFiles.Texture, mip: int) -> list[int]: ...
    @staticmethod
    def GetTexture(ddsfile: list[int]) -> CodeWalker.GameFiles.Texture: ...
    @staticmethod
    def GetTextureFormat(f: DDSIO.DXGI_FORMAT) -> CodeWalker.GameFiles.TextureFormat: ...
    def GetType(self) -> Any: ...
    def ToString(self) -> str: ...

    class CP_FLAGS(IntEnum):
        CP_FLAGS_NONE = 0
        CP_FLAGS_LEGACY_DWORD = 1
        CP_FLAGS_PARAGRAPH = 2
        CP_FLAGS_YMM = 4
        CP_FLAGS_ZMM = 8
        CP_FLAGS_PAGE4K = 512
        CP_FLAGS_24BPP = 65536
        CP_FLAGS_16BPP = 131072
        CP_FLAGS_8BPP = 262144

    class DDS_FLAGS(IntEnum):
        DDS_FLAGS_NONE = 0
        DDS_FLAGS_LEGACY_DWORD = 1
        DDS_FLAGS_NO_LEGACY_EXPANSION = 2
        DDS_FLAGS_NO_R10B10G10A2_FIXUP = 4
        DDS_FLAGS_FORCE_RGB = 8
        DDS_FLAGS_NO_16BPP = 16
        DDS_FLAGS_EXPAND_LUMINANCE = 32
        DDS_FLAGS_FORCE_DX10_EXT = 65536
        DDS_FLAGS_FORCE_DX10_EXT_MISC2 = 131072

    class DDS_HEADER:
        dwSize: int
        dwFlags: int
        dwHeight: int
        dwWidth: int
        dwPitchOrLinearSize: int
        dwDepth: int
        dwMipMapCount: int
        ddspf: DDSIO.DDS_PIXELFORMAT
        dwCaps: int
        dwCaps2: int
        dwCaps3: int
        dwCaps4: int
        dwReserved2: int
        def Equals(self, obj: Any) -> bool: ...
        def GetHashCode(self) -> int: ...
        def GetType(self) -> Any: ...
        def ToString(self) -> str: ...

    class DDS_HEADER_DXT10:
        dxgiFormat: DDSIO.DXGI_FORMAT
        resourceDimension: int
        miscFlag: int
        arraySize: int
        miscFlags2: int
        def Equals(self, obj: Any) -> bool: ...
        def GetHashCode(self) -> int: ...
        def GetType(self) -> Any: ...
        def ToString(self) -> str: ...

    class DDS_PIXELFORMAT:
        dwSize: int
        dwFlags: int
        dwFourCC: int
        dwRGBBitCount: int
        dwRBitMask: int
        dwGBitMask: int
        dwBBitMask: int
        dwABitMask: int
        DDS_FOURCC: ClassVar[int]
        DDS_RGB: ClassVar[int]
        DDS_RGBA: ClassVar[int]
        DDS_LUMINANCE: ClassVar[int]
        DDS_LUMINANCEA: ClassVar[int]
        DDS_ALPHA: ClassVar[int]
        DDS_PAL8: ClassVar[int]
        DDSPF_DXT1: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_DXT2: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_DXT3: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_DXT4: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_DXT5: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_BC4_UNORM: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_BC4_SNORM: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_BC5_UNORM: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_BC5_SNORM: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_R8G8_B8G8: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_G8R8_G8B8: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_YUY2: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_A8R8G8B8: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_X8R8G8B8: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_A8B8G8R8: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_X8B8G8R8: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_G16R16: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_R5G6B5: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_A1R5G5B5: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_A4R4G4B4: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_R8G8B8: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_L8: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_L16: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_A8L8: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_A8: ClassVar[DDSIO.DDS_PIXELFORMAT]
        DDSPF_DX10: ClassVar[DDSIO.DDS_PIXELFORMAT]
        @overload
        def __init__(self, val: int) -> None: ...
        @overload
        def __init__(self, size: int, flags: int, fourcc: int, rgbbitcount: int, rmask: int, gmask: int, bmask: int, amask: int) -> None: ...
        def Equals(self, obj: Any) -> bool: ...
        def GetDXGIFormat(self) -> DDSIO.DXGI_FORMAT: ...
        def GetHashCode(self) -> int: ...
        def GetType(self) -> Any: ...
        @staticmethod
        def MAKEFOURCC(ch0: Any, ch1: Any, ch2: Any, ch3: Any) -> int: ...
        def ToString(self) -> str: ...

    class DXGI_FORMAT(IntEnum):
        DXGI_FORMAT_UNKNOWN = 0
        DXGI_FORMAT_R32G32B32A32_TYPELESS = 1
        DXGI_FORMAT_R32G32B32A32_FLOAT = 2
        DXGI_FORMAT_R32G32B32A32_UINT = 3
        DXGI_FORMAT_R32G32B32A32_SINT = 4
        DXGI_FORMAT_R32G32B32_TYPELESS = 5
        DXGI_FORMAT_R32G32B32_FLOAT = 6
        DXGI_FORMAT_R32G32B32_UINT = 7
        DXGI_FORMAT_R32G32B32_SINT = 8
        DXGI_FORMAT_R16G16B16A16_TYPELESS = 9
        DXGI_FORMAT_R16G16B16A16_FLOAT = 10
        DXGI_FORMAT_R16G16B16A16_UNORM = 11
        DXGI_FORMAT_R16G16B16A16_UINT = 12
        DXGI_FORMAT_R16G16B16A16_SNORM = 13
        DXGI_FORMAT_R16G16B16A16_SINT = 14
        DXGI_FORMAT_R32G32_TYPELESS = 15
        DXGI_FORMAT_R32G32_FLOAT = 16
        DXGI_FORMAT_R32G32_UINT = 17
        DXGI_FORMAT_R32G32_SINT = 18
        DXGI_FORMAT_R32G8X24_TYPELESS = 19
        DXGI_FORMAT_D32_FLOAT_S8X24_UINT = 20
        DXGI_FORMAT_R32_FLOAT_X8X24_TYPELESS = 21
        DXGI_FORMAT_X32_TYPELESS_G8X24_UINT = 22
        DXGI_FORMAT_R10G10B10A2_TYPELESS = 23
        DXGI_FORMAT_R10G10B10A2_UNORM = 24
        DXGI_FORMAT_R10G10B10A2_UINT = 25
        DXGI_FORMAT_R11G11B10_FLOAT = 26
        DXGI_FORMAT_R8G8B8A8_TYPELESS = 27
        DXGI_FORMAT_R8G8B8A8_UNORM = 28
        DXGI_FORMAT_R8G8B8A8_UNORM_SRGB = 29
        DXGI_FORMAT_R8G8B8A8_UINT = 30
        DXGI_FORMAT_R8G8B8A8_SNORM = 31
        DXGI_FORMAT_R8G8B8A8_SINT = 32
        DXGI_FORMAT_R16G16_TYPELESS = 33
        DXGI_FORMAT_R16G16_FLOAT = 34
        DXGI_FORMAT_R16G16_UNORM = 35
        DXGI_FORMAT_R16G16_UINT = 36
        DXGI_FORMAT_R16G16_SNORM = 37
        DXGI_FORMAT_R16G16_SINT = 38
        DXGI_FORMAT_R32_TYPELESS = 39
        DXGI_FORMAT_D32_FLOAT = 40
        DXGI_FORMAT_R32_FLOAT = 41
        DXGI_FORMAT_R32_UINT = 42
        DXGI_FORMAT_R32_SINT = 43
        DXGI_FORMAT_R24G8_TYPELESS = 44
        DXGI_FORMAT_D24_UNORM_S8_UINT = 45
        DXGI_FORMAT_R24_UNORM_X8_TYPELESS = 46
        DXGI_FORMAT_X24_TYPELESS_G8_UINT = 47
        DXGI_FORMAT_R8G8_TYPELESS = 48
        DXGI_FORMAT_R8G8_UNORM = 49
        DXGI_FORMAT_R8G8_UINT = 50
        DXGI_FORMAT_R8G8_SNORM = 51
        DXGI_FORMAT_R8G8_SINT = 52
        DXGI_FORMAT_R16_TYPELESS = 53
        DXGI_FORMAT_R16_FLOAT = 54
        DXGI_FORMAT_D16_UNORM = 55
        DXGI_FORMAT_R16_UNORM = 56
        DXGI_FORMAT_R16_UINT = 57
        DXGI_FORMAT_R16_SNORM = 58
        DXGI_FORMAT_R16_SINT = 59
        DXGI_FORMAT_R8_TYPELESS = 60
        DXGI_FORMAT_R8_UNORM = 61
        DXGI_FORMAT_R8_UINT = 62
        DXGI_FORMAT_R8_SNORM = 63
        DXGI_FORMAT_R8_SINT = 64
        DXGI_FORMAT_A8_UNORM = 65
        DXGI_FORMAT_R1_UNORM = 66
        DXGI_FORMAT_R9G9B9E5_SHAREDEXP = 67
        DXGI_FORMAT_R8G8_B8G8_UNORM = 68
        DXGI_FORMAT_G8R8_G8B8_UNORM = 69
        DXGI_FORMAT_BC1_TYPELESS = 70
        DXGI_FORMAT_BC1_UNORM = 71
        DXGI_FORMAT_BC1_UNORM_SRGB = 72
        DXGI_FORMAT_BC2_TYPELESS = 73
        DXGI_FORMAT_BC2_UNORM = 74
        DXGI_FORMAT_BC2_UNORM_SRGB = 75
        DXGI_FORMAT_BC3_TYPELESS = 76
        DXGI_FORMAT_BC3_UNORM = 77
        DXGI_FORMAT_BC3_UNORM_SRGB = 78
        DXGI_FORMAT_BC4_TYPELESS = 79
        DXGI_FORMAT_BC4_UNORM = 80
        DXGI_FORMAT_BC4_SNORM = 81
        DXGI_FORMAT_BC5_TYPELESS = 82
        DXGI_FORMAT_BC5_UNORM = 83
        DXGI_FORMAT_BC5_SNORM = 84
        DXGI_FORMAT_B5G6R5_UNORM = 85
        DXGI_FORMAT_B5G5R5A1_UNORM = 86
        DXGI_FORMAT_B8G8R8A8_UNORM = 87
        DXGI_FORMAT_B8G8R8X8_UNORM = 88
        DXGI_FORMAT_R10G10B10_XR_BIAS_A2_UNORM = 89
        DXGI_FORMAT_B8G8R8A8_TYPELESS = 90
        DXGI_FORMAT_B8G8R8A8_UNORM_SRGB = 91
        DXGI_FORMAT_B8G8R8X8_TYPELESS = 92
        DXGI_FORMAT_B8G8R8X8_UNORM_SRGB = 93
        DXGI_FORMAT_BC6H_TYPELESS = 94
        DXGI_FORMAT_BC6H_UF16 = 95
        DXGI_FORMAT_BC6H_SF16 = 96
        DXGI_FORMAT_BC7_TYPELESS = 97
        DXGI_FORMAT_BC7_UNORM = 98
        DXGI_FORMAT_BC7_UNORM_SRGB = 99
        DXGI_FORMAT_AYUV = 100
        DXGI_FORMAT_Y410 = 101
        DXGI_FORMAT_Y416 = 102
        DXGI_FORMAT_NV12 = 103
        DXGI_FORMAT_P010 = 104
        DXGI_FORMAT_P016 = 105
        DXGI_FORMAT_420_OPAQUE = 106
        DXGI_FORMAT_YUY2 = 107
        DXGI_FORMAT_Y210 = 108
        DXGI_FORMAT_Y216 = 109
        DXGI_FORMAT_NV11 = 110
        DXGI_FORMAT_AI44 = 111
        DXGI_FORMAT_IA44 = 112
        DXGI_FORMAT_P8 = 113
        DXGI_FORMAT_A8P8 = 114
        DXGI_FORMAT_B4G4R4A4_UNORM = 115
        XBOX_DXGI_FORMAT_R10G10B10_7E3_A2_FLOAT = 116
        XBOX_DXGI_FORMAT_R10G10B10_6E4_A2_FLOAT = 117
        XBOX_DXGI_FORMAT_D16_UNORM_S8_UINT = 118
        XBOX_DXGI_FORMAT_R16_UNORM_X8_TYPELESS = 119
        XBOX_DXGI_FORMAT_X16_TYPELESS_G8_UINT = 120
        WIN10_DXGI_FORMAT_P208 = 130
        WIN10_DXGI_FORMAT_V208 = 131
        WIN10_DXGI_FORMAT_V408 = 132
        XBOX_DXGI_FORMAT_R10G10B10_SNORM_A2_UNORM = 189
        XBOX_DXGI_FORMAT_R4G4_UNORM = 190
        DXGI_FORMAT_FORCE_UINT = 4294967295

    class DXTex:
        DDS_HEADER_FLAGS_TEXTURE: ClassVar[int]
        DDS_HEADER_FLAGS_MIPMAP: ClassVar[int]
        DDS_HEADER_FLAGS_VOLUME: ClassVar[int]
        DDS_HEADER_FLAGS_PITCH: ClassVar[int]
        DDS_HEADER_FLAGS_LINEARSIZE: ClassVar[int]
        DDS_HEIGHT: ClassVar[int]
        DDS_WIDTH: ClassVar[int]
        DDS_SURFACE_FLAGS_TEXTURE: ClassVar[int]
        DDS_SURFACE_FLAGS_MIPMAP: ClassVar[int]
        DDS_SURFACE_FLAGS_CUBEMAP: ClassVar[int]
        DDS_CUBEMAP_POSITIVEX: ClassVar[int]
        DDS_CUBEMAP_NEGATIVEX: ClassVar[int]
        DDS_CUBEMAP_POSITIVEY: ClassVar[int]
        DDS_CUBEMAP_NEGATIVEY: ClassVar[int]
        DDS_CUBEMAP_POSITIVEZ: ClassVar[int]
        DDS_CUBEMAP_NEGATIVEZ: ClassVar[int]
        DDS_CUBEMAP_ALLFACES: ClassVar[int]
        DDS_CUBEMAP: ClassVar[int]
        DDS_FLAGS_VOLUME: ClassVar[int]
        DDS_MAGIC: ClassVar[int]
        @staticmethod
        def BitsPerPixel(fmt: DDSIO.DXGI_FORMAT) -> int: ...
        @staticmethod
        def ComputePitch(fmt: DDSIO.DXGI_FORMAT, width: int, height: int, rowPitch: int, slicePitch: int, flags: int) -> None: ...
        @staticmethod
        def ComputeScanlines(fmt: DDSIO.DXGI_FORMAT, height: int) -> int: ...
        def Equals(self, obj: Any) -> bool: ...
        def GetHashCode(self) -> int: ...
        def GetType(self) -> Any: ...
        @staticmethod
        def IsCompressed(fmt: DDSIO.DXGI_FORMAT) -> bool: ...
        @staticmethod
        def IsPacked(fmt: DDSIO.DXGI_FORMAT) -> bool: ...
        @staticmethod
        def IsPalettized(fmt: DDSIO.DXGI_FORMAT) -> bool: ...
        @staticmethod
        def IsPlanar(fmt: DDSIO.DXGI_FORMAT) -> bool: ...
        @staticmethod
        def IsValid(fmt: DDSIO.DXGI_FORMAT) -> bool: ...
        def ToString(self) -> str: ...
        @staticmethod
        def assert_(b: bool) -> None: ...

    class Image:
        width: int
        height: int
        format: DDSIO.DXGI_FORMAT
        rowPitch: int
        slicePitch: int
        pixels: int
        def Equals(self, obj: Any) -> bool: ...
        def GetHashCode(self) -> int: ...
        def GetType(self) -> Any: ...
        def ToString(self) -> str: ...

    class ImageStruct:
        Width: int
        Height: int
        Format: int
        MipMapLevels: int
        Data: list[int]
        def __init__(self) -> None: ...
        def Equals(self, obj: Any) -> bool: ...
        def GetHashCode(self) -> int: ...
        def GetType(self) -> Any: ...
        def ToString(self) -> str: ...

    class TEX_ALPHA_MODE(IntEnum):
        TEX_ALPHA_MODE_UNKNOWN = 0
        TEX_ALPHA_MODE_STRAIGHT = 1
        TEX_ALPHA_MODE_PREMULTIPLIED = 2
        TEX_ALPHA_MODE_OPAQUE = 3
        TEX_ALPHA_MODE_CUSTOM = 4

    class TEX_DIMENSION(IntEnum):
        TEX_DIMENSION_TEXTURE1D = 2
        TEX_DIMENSION_TEXTURE2D = 3
        TEX_DIMENSION_TEXTURE3D = 4

    class TEX_MISC_FLAG(IntEnum):
        TEX_MISC_TEXTURECUBE = 4
        TEX_MISC2_ALPHA_MODE_MASK = 7

    class TexMetadata:
        width: int
        height: int
        depth: int
        arraySize: int
        mipLevels: int
        miscFlags: int
        miscFlags2: int
        format: DDSIO.DXGI_FORMAT
        dimension: DDSIO.TEX_DIMENSION
        def ComputeIndex(self, mip: int, item: int, slice: int) -> int: ...
        def Equals(self, obj: Any) -> bool: ...
        def GetHashCode(self) -> int: ...
        def GetType(self) -> Any: ...
        def IsCubemap(self) -> bool: ...
        def IsPMAlpha(self) -> bool: ...
        def IsVolumemap(self) -> bool: ...
        def ToString(self) -> str: ...
