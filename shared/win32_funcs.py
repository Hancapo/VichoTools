import ctypes
from ctypes import wintypes

CLSID_FileOpenDialog = ctypes.c_byte * 16
IID_IFileOpenDialog = ctypes.c_byte * 16
IID_IShellItem = ctypes.c_byte * 16

def guid_bytes(guid):
    import uuid
    return (ctypes.c_byte * 16).from_buffer_copy(uuid.UUID(guid).bytes_le)

CLSID_FileOpenDialog = guid_bytes("DC1C5A9C-E88A-4DDE-A5A1-60F82A20AEF7")
IID_IFileOpenDialog = guid_bytes("D57C7288-D4AD-4768-BE02-9D969532D960")

CLSCTX_INPROC_SERVER = 1
FOS_PICKFOLDERS = 0x00000020
FOS_FORCEFILESYSTEM = 0x00000040
FOS_PATHMUSTEXIST = 0x00000800
SIGDN_FILESYSPATH = 0x80058000

ole32 = ctypes.windll.ole32

def select_folder(title="Select Folder") -> str | None:
    ole32.CoInitialize(None)

    dialog = ctypes.c_void_p()
    hr = ole32.CoCreateInstance(
        ctypes.byref(CLSID_FileOpenDialog),
        None,
        CLSCTX_INPROC_SERVER,
        ctypes.byref(IID_IFileOpenDialog),
        ctypes.byref(dialog)
    )

    if hr != 0:
        return None

    vtbl = ctypes.cast(dialog, ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p))).contents

    Show = ctypes.WINFUNCTYPE(wintypes.HRESULT, ctypes.c_void_p, wintypes.HWND)(vtbl[3])
    SetOptions = ctypes.WINFUNCTYPE(wintypes.HRESULT, ctypes.c_void_p, wintypes.DWORD)(vtbl[9])
    SetTitle = ctypes.WINFUNCTYPE(wintypes.HRESULT, ctypes.c_void_p, wintypes.LPCWSTR)(vtbl[17])
    GetResult = ctypes.WINFUNCTYPE(wintypes.HRESULT, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p))(vtbl[20])
    Release = ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)(vtbl[2])

    SetOptions(dialog, FOS_PICKFOLDERS | FOS_FORCEFILESYSTEM | FOS_PATHMUSTEXIST)
    SetTitle(dialog, title)

    hr = Show(dialog, None)

    if hr != 0:
        Release(dialog)
        ole32.CoUninitialize()
        return None

    item = ctypes.c_void_p()
    GetResult(dialog, ctypes.byref(item))

    item_vtbl = ctypes.cast(item, ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p))).contents

    GetDisplayName = ctypes.WINFUNCTYPE(
        wintypes.HRESULT,
        ctypes.c_void_p,
        ctypes.c_uint,
        ctypes.POINTER(ctypes.c_wchar_p)
    )(item_vtbl[5])

    item_release = ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)(item_vtbl[2])

    path_ptr = ctypes.c_wchar_p()
    GetDisplayName(item, SIGDN_FILESYSPATH, ctypes.byref(path_ptr))

    path = path_ptr.value

    ole32.CoTaskMemFree(path_ptr)
    item_release(item)
    Release(dialog)
    ole32.CoUninitialize()
    return path