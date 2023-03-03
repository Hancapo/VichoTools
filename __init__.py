import bpy
from .utils.ytd_helper import *
from .utils.vicho_funcs import *
from .utils.vicho_operators import *
from .utils.vicho_panels import *
from .utils.folders2ytd import *

bl_info = {
    "name": "Vicho's Misc Tools",
    "author": "MrVicho13",
    "version": (0, 2, 0),
    "blender": (3, 0, 0),
    "location": "View3D",
    "description": "Some tools by Vicho",
    "warning": "",
    "wiki_url": "",
    "category": "Vicho Tools",
}


vicho_classes = [
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
    VichoToolsAddonProperties,
    YTDLIST_OT_add,
    YTDLIST_OT_remove,
    YTDLIST_OT_reload_all,
    YTDLIST_OT_add_to_ytd,
    YTDLIST_OT_assign_ytd_field_from_list,
    ExportYTDFolders,
    ExportYTDFiles
]


def register():
    for klass in vicho_classes:
        bpy.utils.register_class(klass)

    bpy.types.Scene.ytd_list = bpy.props.CollectionProperty(type=YtdItem)
    bpy.types.Scene.ytd_active_index = bpy.props.IntProperty()


def unregister():
    for klass in vicho_classes:
        bpy.utils.unregister_class(klass)

    del bpy.types.Scene.ytd_list
    del bpy.types.Scene.ytd_active_index


if __name__ == '__main__':
    register()
