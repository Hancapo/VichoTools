import bpy
from bpy.app.handlers import persistent


COMPAT_SOLL: list[str] = [
            "sollumz_drawable",
            "sollumz_fragment",
            "sollumz_drawable_model",
            "sollumz_drawable_dictionary",
        ]


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
            if mesh.mesh is None or (
                mesh.mesh.name not in bpy.context.view_layer.objects
                and not is_obj_in_any_collection(mesh.mesh)
            ):
                if (
                    mesh.mesh
                    and mesh.mesh.name not in bpy.context.view_layer.objects
                    and not is_obj_in_any_collection(mesh.mesh)
                ):
                    bpy.data.objects.remove(mesh.mesh, do_unlink=True)
                ytd.mesh_list.remove(mesh_index)
                switch_ytd_selected_index(scene)

        if len(ytd.mesh_list) == 0:
            scene.ytd_list.remove(ytd_index)
            switch_ytd_selected_index(scene)


def switch_ytd_selected_index(scene):
    if len(scene.ytd_list) != 0:
        if len(scene.ytd_list[scene.ytd_active_index].mesh_list) < 1:
            scene.ytd_active_index = 0 if len(scene.ytd_list) > 0 else -1


@persistent
def update_post(scene, depsgraph):
    remove_invalid_meshes(scene)
