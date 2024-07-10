import bpy
from bpy.app.handlers import persistent
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
                if item is not None and item.mesh is not None:
                    row.prop(item.mesh, "name", text="", emboss=False, icon='MESH_CUBE')

class MaterialProp(bpy.types.PropertyGroup):
    material: bpy.props.PointerProperty(type=bpy.types.Material) # type: ignore


class MeshGroup(bpy.types.PropertyGroup):
    mesh: bpy.props.PointerProperty(type=bpy.types.Object) # type: ignore

class YtdItem(bpy.types.PropertyGroup):
    material_list: bpy.props.CollectionProperty(type=MaterialProp)
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

def is_obj_in_any_collection(obj):
    return any(obj.name in collection.objects for collection in bpy.data.collections)


def remove_invalid_meshes(scene):
    for ytd_index in reversed(range(len(scene.ytd_list))):
        ytd = scene.ytd_list[ytd_index]
        for mesh_index, mesh in reversed(list(enumerate(ytd.mesh_list))):
            if mesh.mesh is None or (mesh.mesh.name not in bpy.context.view_layer.objects and not is_obj_in_any_collection(mesh.mesh)):
                if mesh.mesh and mesh.mesh.name not in bpy.context.view_layer.objects and not is_obj_in_any_collection(mesh.mesh):
                    bpy.data.objects.remove(mesh.mesh, do_unlink=True)
                ytd.mesh_list.remove(mesh_index)
                switch_ytd_selected_index(scene)
                
        if len(ytd.mesh_list) == 0:
            scene.ytd_list.remove(ytd_index)
            switch_ytd_selected_index(scene)
            
    

def switch_ytd_selected_index(scene):
    if len(scene.ytd_list[scene.ytd_active_index].mesh_list) < 1:
        scene.ytd_active_index = 0 if len(scene.ytd_list) > 0 else -1
    else:
        scene.ytd_active_index = scene.ytd_active_index

@persistent
def update_mesh_list(scene, depsgraph):
    remove_invalid_meshes(scene)
