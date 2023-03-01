import bpy
import os
from mathutils import Quaternion
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from .utils.ytd_helper import *
from .utils.vicho_funcs import *
import subprocess
from .utils.vicho_operators import *
from .utils.vicho_panels import *

bl_info = {
    "name": "Vicho's Misc Tools",
    "author": "Somebody",
    "version": (0, 1, 6),
    "blender": (3, 0, 0),
    "location": "View3D",
    "description": "Some tools by Vicho",
    "warning": "",
    "wiki_url": "",
    "category": "Vicho Tools",
}


CLASSES = [
    VICHO_PT_MAIN_PANEL,
    ExpSelObjsFile,
    ResetObjTransRot,
    ExportMLOTransFile,
    DeleteEmptyObj,
    VICHO_PT_MISC1_PANEL,
    VichoMloToolsPanel,
    VichoObjectToolsPanel,
    PasteObjectTransformFromPickedObject,
    MloYmapFileBrowser,
    Vicho_PT_vertex_color,
    VichoCreateVC,
    Vicho_TextureDictionaryPanel,
    MeshGroup,
    ImageString,
    YtdList,
    YtdItem,
    YTDLIST_OT_add,
    YTDLIST_OT_remove,
    YTDLIST_OT_reloadall,
    YtdExportPath
]


def register():
    for klass in CLASSES:
        bpy.utils.register_class(klass)

    bpy.types.Scene.ytd_list = bpy.props.CollectionProperty(type=YtdItem)
    bpy.types.Scene.ytd_active_index = bpy.props.IntProperty()


def unregister():
    for klass in CLASSES:
        bpy.utils.unregister_class(klass)

    del bpy.types.Scene.ytd_list
    del bpy.types.Scene.ytd_active_index


if __name__ == '__main__':
    register()
