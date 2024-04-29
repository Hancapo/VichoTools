import bpy
class YTDLIST_UL_list(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(item, "selected", text="", emboss=False, icon='CHECKBOX_HLT' if item.selected else 'CHECKBOX_DEHLT')
            row.prop(item, "name", text="", emboss=False, icon='IMAGE_BACKGROUND')
            row = layout.row(align=True)
            row.scale_x = 0.7
            row.prop(item, "game_target", text="", emboss=False, icon="MATSHADERBALL")

class MESHLIST_UL_list(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if len(context.scene.ytd_list) != 0:
                row = layout.row(align=True)
                row.label(text=item.mesh.name, icon='MESH_DATA')

class ImageString(bpy.types.PropertyGroup):
    filepath: bpy.props.StringProperty() # type: ignore


class MeshGroup(bpy.types.PropertyGroup):
    mesh: bpy.props.PointerProperty(type=bpy.types.Object) # type: ignore


class YtdItem(bpy.types.PropertyGroup):
    image_list: bpy.props.CollectionProperty(type=ImageString)
    mesh_list: bpy.props.CollectionProperty(type=MeshGroup)
    selected: bpy.props.BoolProperty(default=True, name="Selection")
    game_target: bpy.props.EnumProperty(
        items=[('GTA5', 'GTA 5', 'Grand Theft Auto V ITD')], default='GTA5', name='Game Target') # type: ignore
    
def ytd_index_changed(self, context):
    if len(self.ytd_list) != 0:
        selected_item = self.ytd_list[self.ytd_active_index]
        self.mesh_list.clear()
        for mesh in selected_item.mesh_list:
            new_mesh = self.mesh_list.add()
            new_mesh.mesh = mesh.mesh



