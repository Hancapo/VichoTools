import bpy
from .helper import ytd_index_changed, update_post


class MaterialProp(bpy.types.PropertyGroup):
    material: bpy.props.PointerProperty(type=bpy.types.Material)  # type: ignore


class MeshGroup(bpy.types.PropertyGroup):
    mesh: bpy.props.PointerProperty(type=bpy.types.Object)  # type: ignore


class YtdItem(bpy.types.PropertyGroup):
    material_list: bpy.props.CollectionProperty(type=MaterialProp)
    mesh_list: bpy.props.CollectionProperty(type=MeshGroup)
    selected: bpy.props.BoolProperty(default=True, name="Check")
    game_target: bpy.props.EnumProperty(
        items=[("GTA5", "GTA 5", "Grand Theft Auto V ITD")],
        default="GTA5",
        name="Game Target",
    )  # type: ignore


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
