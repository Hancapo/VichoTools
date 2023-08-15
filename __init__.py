import bpy

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
    "name": "Vicho's Misc Tools",
    "author": "MrVicho13",
    "version": (0, 3, 3),
    "blender": (3, 0, 0),
    "location": "View3D",
    "description": "Some tools by Vicho",
    "warning": "",
    "wiki_url": "",
    "category": "Vicho Tools",
}

vicho_classes = [
    ExpSelObjsFile,
    ResetObjTransRot,
    ExportMLOTransFile,
    DeleteEmptyObj,
    VICHO_PT_MISC1_PANEL,
    VichoMloToolsPanel,
    VichoObjectToolsPanel,
    PasteObjectTransformFromPickedObject,
    MloYmapFileBrowser,
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
    ExportYTDFiles,
    
]

def register():
    for _class in vicho_classes:
        bpy.utils.register_class(_class)

    bpy.types.Scene.ytd_list = bpy.props.CollectionProperty(type=YtdItem)
    bpy.types.Scene.ytd_active_index = bpy.props.IntProperty()

def unregister():
    for _class in vicho_classes:
        bpy.utils.unregister_class(_class)

    del bpy.types.Scene.ytd_list
    del bpy.types.Scene.ytd_active_index

if __name__ == '__main__':
    register()
