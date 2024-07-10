import bpy
import itertools
from .vicho_dependencies import *

if depen_installed():
    from .ytd.cw_py.cw_ytd_tools import *

from .ytd.cw_py.cw_py_misc import *
from .misc.misc_funcs import *
from .vicho_operators import *
from .vicho_properties import *
from .vicho_panels import *
from .ytd.operators import *
from .ytd.ui import *
from .vicho_adn_props import VichoToolsAddonProperties

bl_info = {
    "name": "Vicho's Tools",
    "author": "MrVicho13",
    "version": (0, 7, 3),
    "blender": (4, 0, 0),
    "description": "Tools designed to help with GTA V modding",
    "category": "Vicho's Tools",
    "doc_url": "https://sollumz.gitbook.io/sollumz-wiki/",
    "tracker_url": "https://github.com/Hancapo/VichoTools/issues",
}

vicho_classes = [
    VICHO_PT_MISC1_PANEL,
    VichoToolsAddonProperties,
    VichoToolsInstallDependencies,
    VichoToolsInstallDotnetRuntime
]

ytd_classes = [
    Vicho_TextureDictionaryPanel,
    MeshGroup,
    MaterialProp,
    YTDLIST_UL_list,
    MESHLIST_UL_list,
    YtdItem,
    YTDLIST_OT_add,
    YTDLIST_OT_remove,
    YTDLIST_OT_add_to_ytd,
    YTDLIST_OT_assign_ytd_field_from_list,
    YTDLIST_OT_select_meshes_from_ytd_folder,
    YTDLIST_OT_select_mesh_from_ytd_folder,
    YTDLIST_OT_fake_op,
    MESHLIST_OT_confirm_delete_mesh,
    MESHLIST_OT_delete_mesh,
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
    VichoObjectToolsPanel,
    DeleteAllColorAttributes,
    DeleteAllVertexGroups,
    PasteObjectTransformFromPickedObject,
    DetectMeshesWithNoTextures,
    RenameAllUvMaps
]


def register():
    for _class in list(itertools.chain(vicho_classes, misc_classes, obj_classes, mlo_classes, ytd_classes)):
        bpy.utils.register_class(_class)
    bpy.types.Scene.ytd_list = bpy.props.CollectionProperty(type=YtdItem)
    bpy.types.Scene.ytd_active_index = bpy.props.IntProperty(name="Active Index", update=ytd_index_changed)
    bpy.types.Scene.mesh_list = bpy.props.CollectionProperty(type=MeshGroup)
    bpy.types.Scene.mesh_active_index = bpy.props.IntProperty(name="Active Index")
    bpy.app.handlers.depsgraph_update_post.append(update_mesh_list)

def unregister():
    for _class in list(itertools.chain(vicho_classes, misc_classes, obj_classes, mlo_classes, ytd_classes)):
        bpy.utils.unregister_class(_class)
    del bpy.types.Scene.ytd_list
    del bpy.types.Scene.ytd_active_index
    del bpy.types.Scene.mesh_list
    del bpy.types.Scene.mesh_active_index
    bpy.app.handlers.depsgraph_update_post.remove(update_mesh_list)

if __name__ == '__main__':
    register()
