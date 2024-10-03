import bpy
from .helper import ytd_index_changed, update_post

process_type = [
    ("ALL", "All", "ALL"),
    ("CHECKED", "Checked item(s)", "Checked item(s)"),
    ("SELECTED", "Selected item", "Selected item"),
]

quality_settings = [
    (
        "FASTEST",
        "Fastest",
        "Fastest processing time. Results may be reasonable, but is not considered to be real-time either"
    ),
    (
        "NORMAL", 
        "Normal", 
        "Balanced in terms of quality / speed"
    ),
    (
        "PRODUCTION",
        "Production",
        "Generally produces similar results to normal, but it may double or triple the time to obtain minor quality improvements"
    ),
    (
        "HIGHEST",
        "Highest",
        "Slowest processing time. May be extremely slow as it brute force compressor and should generally only be used for testing purposes"
    ),
]

def generate_power_of_two_enum(max_power):
    return [(str(2**i), str(2**i), str(2**i)) for i in range(2, max_power + 1)]



def update_path(self, context):
    if self.ytd_export_path != '':
        self.ytd_export_path = bpy.path.abspath(self.ytd_export_path)


class ImageProp(bpy.types.PropertyGroup):
    """Group of properties for each image in the YTD item, including the image itself and some flags"""
    img_path: bpy.props.StringProperty(name="Image Path", default="")
    img_ext: bpy.props.StringProperty(name="Image Extension", default="")
    img_name: bpy.props.StringProperty(name="Image Name", default="")
    img_name_full: bpy.props.StringProperty(name="Image Name Full", default="")
    
    flag_tint: bpy.props.BoolProperty(default=False, name="Is Tint?")
    flag_0: bpy.props.BoolProperty(default=False, name="Reserved 1")
    flag_1: bpy.props.BoolProperty(default=False, name="Reserved 2")


class MeshGroup(bpy.types.PropertyGroup):
    mesh: bpy.props.PointerProperty(type=bpy.types.Object)  # type: ignore


class YtdItem(bpy.types.PropertyGroup):
    img_data_list: bpy.props.CollectionProperty(type=ImageProp)
    mesh_list: bpy.props.CollectionProperty(type=MeshGroup)
    selected: bpy.props.BoolProperty(default=True, name="Check")
    game_target: bpy.props.EnumProperty(
        items=[("GTA5", "GTA 5", "Grand Theft Auto V ITD")],
        default="GTA5",
        name="Game Target",
    )  # type: ignore


class YtdGroupProps(bpy.types.PropertyGroup):
    bpy.types.Scene.ytd_export_path = bpy.props.StringProperty(
        name="Export Path",
        default="",
        description="Path to export the YTD file(s)",
        subtype="DIR_PATH",
        update=update_path,
    )

    bpy.types.Scene.ytd_enum_process_type = bpy.props.EnumProperty(
        items=process_type,
        name="Process Type",
        default="ALL",
        description="Sets the type of export to perform over the list of texture dictionaries",
    )

    bpy.types.Scene.ytd_show_explorer_after_export = bpy.props.BoolProperty(
        name="Show containing folder after export",
        description="Show the containing folder where the YTD file(s) were exported",
        default=True,
    )

    bpy.types.Scene.ytd_show_mesh_list = bpy.props.BoolProperty(
        name="Show Mesh List",
        description="Show the mesh list from the selected YTD item",
        default=False,
    )

    bpy.types.Scene.dds_conv_quality = bpy.props.EnumProperty(
        items=quality_settings,
        name="Quality",
        default="NORMAL",
        description="Image to DDS conversion quality",
    )

    bpy.types.Scene.ytd_advanced_mode = bpy.props.BoolProperty(
        name="Advanced Mode",
        default=False,
        description="Enable advanced options for resizing textures",
    )

    bpy.types.Scene.max_pixel_size_list = bpy.props.EnumProperty(
        items=generate_power_of_two_enum(12), name="Size", default="1024"
    )
    bpy.types.Scene.max_pixel_size = bpy.props.BoolProperty(
        name="Max Pixel",
        default=False,
        description="Limit all textures' dimensions to the selected value",
    )
    bpy.types.Scene.divide_textures_size = bpy.props.BoolProperty(
        name="Half Texture Size",
        default=False,
        description="Divide all textures' dimensions by 2",
    )


def register():
    bpy.types.Scene.ytd_list = bpy.props.CollectionProperty(type=YtdItem)
    bpy.types.Scene.ytd_active_index = bpy.props.IntProperty(
        name="Active Index", update=ytd_index_changed
    )
    bpy.types.Scene.mesh_list = bpy.props.CollectionProperty(type=MeshGroup)
    bpy.types.Scene.mesh_active_index = bpy.props.IntProperty(name="Active Index")
    bpy.app.handlers.depsgraph_update_post.append(update_post)


def unregister():
    del bpy.types.Scene.ytd_list
    del bpy.types.Scene.ytd_active_index
    del bpy.types.Scene.mesh_list
    del bpy.types.Scene.mesh_active_index
    bpy.app.handlers.depsgraph_update_post.remove(update_post)
