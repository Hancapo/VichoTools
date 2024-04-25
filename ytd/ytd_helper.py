import bpy
class YtdList(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(item, "selected", text="", emboss=False, icon='CHECKBOX_HLT' if item.selected else 'CHECKBOX_DEHLT')
            row.prop(item, "name", text="", emboss=False, icon='IMAGE_BACKGROUND')
            row = layout.row(align=True)
            row.scale_x = 0.7
            row.label(text=f"{len(item.mesh_list)}", icon='MESH_DATA')
            row.prop(item, "game_target", text="", emboss=False, icon="MATSHADERBALL")



class ImageString(bpy.types.PropertyGroup):
    filepath: bpy.props.StringProperty() # type: ignore


class MeshGroup(bpy.types.PropertyGroup):
    mesh: bpy.props.PointerProperty(type=bpy.types.Object) # type: ignore


class YtdItem(bpy.types.PropertyGroup):
    image_list: bpy.props.CollectionProperty(type=ImageString)
    mesh_list: bpy.props.CollectionProperty(type=MeshGroup)
    selected: bpy.props.BoolProperty(default=True, name="Selection")
    game_target: bpy.props.EnumProperty(
        items=[('GTA5', 'GTA 5', 'Grand Theft Auto V YTD')], default='GTA5', name='Game Target') # type: ignore
    






