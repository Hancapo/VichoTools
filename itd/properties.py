import bpy

from ..shared.funcs import generate_power_of_two_enum
from .helper import update_post_itd, update_itd_path, itd_index_changed, update_dds_quality
from .constants import ITD_MENU_ENUM, GAME_TYPES, PROCESS_TYPE, DDS_QUALITY_ITEMS


class ImageProp(bpy.types.PropertyGroup):
    """Group of properties for each image in the YTD item, including the image itself and some flags"""

    img_path: bpy.props.StringProperty(name="Image Path", default="")  # type: ignore
    img_ext: bpy.props.StringProperty(name="Image Extension", default="")  # type: ignore
    img_name: bpy.props.StringProperty(name="Image Name", default="")  # type: ignore
    img_name_full: bpy.props.StringProperty(name="Image Name Full", default="")  # type: ignore

    flag_tint: bpy.props.BoolProperty(default=False, name="Is Tint?")  # type: ignore
    flag_0: bpy.props.BoolProperty(default=False, name="Reserved 1")  # type: ignore
    flag_1: bpy.props.BoolProperty(default=False, name="Reserved 2")  # type: ignore


class MeshGroup(bpy.types.PropertyGroup):
    mesh: bpy.props.PointerProperty(type=bpy.types.Object)  # type: ignore


class ItdItem(bpy.types.PropertyGroup):
    img_data_list: bpy.props.CollectionProperty(type=ImageProp)  # type: ignore
    mesh_list: bpy.props.CollectionProperty(type=MeshGroup)  # type: ignore
    selected: bpy.props.BoolProperty(default=True, name="Check")  # type: ignore
    game_target: bpy.props.EnumProperty(
        items=GAME_TYPES,
        default="GTA5_GEN8",
        name="Game Target",
    )  # type: ignore

    dds_conv_quality: bpy.props.EnumProperty(
    name="DDS Quality",
    description="DDS conversion quality preset",
    items=DDS_QUALITY_ITEMS,
    default="1.0",
    
    ) # type: ignore
    max_pixel_size: bpy.props.EnumProperty(
        items=[("NO_LIMIT", "No Limit", "no limit")] + generate_power_of_two_enum(13), name="Size", default="NO_LIMIT"
    )  # type: ignore
    adv_toggle: bpy.props.BoolProperty(
        name="Advanced Mode",
        default=False,
        description="Enable advanced options for ITD's textures resizing",
    )  # type: ignore

class YtdGroupProps(bpy.types.PropertyGroup):
    bpy.types.Scene.itd_export_path = bpy.props.StringProperty(
        name="Export Path",
        default="",
        description="Path to export the ITD file(s)",
        subtype="DIR_PATH",
        update=lambda self, context: update_itd_path(self, context),
    )

    bpy.types.Scene.itd_enum_process_type = bpy.props.EnumProperty(
        items=PROCESS_TYPE,
        name="Process Type",
        default="ALL",
        description="Sets the type of export to perform over the list of texture dictionaries",
    )

    bpy.types.Scene.itd_show_explorer_after_export = bpy.props.BoolProperty(
        name="Show containing folder after export",
        description="Show the containing folder where the ITD file(s) were exported",
        default=True,
    )

    bpy.types.Scene.itd_show_mesh_list = bpy.props.BoolProperty(
        name="Show Mesh List",
        description="Show the mesh list from the selected ITD item",
        default=False,
    )


def register():
    bpy.types.Scene.itd_list = bpy.props.CollectionProperty(type=ItdItem)
    bpy.types.Scene.itd_active_index = bpy.props.IntProperty(
        name="Active Index", update=itd_index_changed
    )
    bpy.types.Scene.mesh_list = bpy.props.CollectionProperty(type=MeshGroup)
    bpy.types.Scene.mesh_active_index = bpy.props.IntProperty(name="Active Index")
    bpy.types.Scene.itd_menu = bpy.props.EnumProperty(
        items=ITD_MENU_ENUM,
        name="ITD Menu",
        default="SETTINGS",
    )
    bpy.app.handlers.depsgraph_update_post.append(update_post_itd)


def unregister():
    del bpy.types.Scene.itd_list
    del bpy.types.Scene.itd_active_index
    del bpy.types.Scene.mesh_list
    del bpy.types.Scene.mesh_active_index
    del bpy.types.Scene.itd_menu
    bpy.app.handlers.depsgraph_update_post.remove(update_post_itd)
