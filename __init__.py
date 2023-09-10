import bpy
import itertools
from .ytd.ytd_helper import *
from .misc.misc_funcs import *
from .vicho_operators import *
from .vicho_properties import *
from .vicho_panels import *
from .ytd.folders2ytd import *
from .ytd.operators import *
from .ytd.ui import *
from .vicho_misc import VichoToolsAddonProperties

bl_info = {
    "name": "Vicho's Tools",
    "author": "MrVicho13",
    "version": (0, 4, 5),
    "blender": (3, 0, 0),
    "location": "View3D",
    "description": "Tools designed to help with GTA V modding",
    "warning": "",
    "wiki_url": "",
    "category": "Vicho's Tools",
}

vicho_classes = [
    VICHO_PT_MISC1_PANEL,
    VichoToolsAddonProperties,
]

ytd_classes = [
    Vicho_TextureDictionaryPanel,
    MeshGroup,
    ImageString,
    YtdList,
    YtdItem,
    YTDLIST_OT_add,
    YTDLIST_OT_remove,
    YTDLIST_OT_reload_all,
    YTDLIST_OT_add_to_ytd,
    YTDLIST_OT_assign_ytd_field_from_list,
    ExportYTDFolders,
    ExportYTDFiles,
]

misc_classes = [
    ExpSelObjsFile,
]

mlo_classes = [
    ExportMLOTransFile,
    VichoMloToolsPanel,
    MloYmapFileBrowser,
]

obj_classes = [
    ResetObjTransRot,
    DeleteEmptyObj,
    VichoObjectToolsPanel,
    DeleteAllColorAttributes,
    DeleteAllVertexGroups,
    PasteObjectTransformFromPickedObject,
    DetectMeshesWithNoTextures
]


def register():
    for _class in list(itertools.chain(vicho_classes, misc_classes, obj_classes, mlo_classes, ytd_classes)):
        bpy.utils.register_class(_class)

    bpy.types.Scene.ytd_list = bpy.props.CollectionProperty(type=YtdItem)
    bpy.types.Scene.ytd_active_index = bpy.props.IntProperty()


def unregister():
    for _class in list(itertools.chain(vicho_classes, misc_classes, obj_classes, mlo_classes, ytd_classes)):
        bpy.utils.unregister_class(_class)

    del bpy.types.Scene.ytd_list
    del bpy.types.Scene.ytd_active_index


if __name__ == '__main__':
    register()
