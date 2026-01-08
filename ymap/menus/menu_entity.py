import bpy
from ..operators.operators_entity import VICHO_OT_export_entity_asset, VICHO_OT_invert_entity_selection, VICHO_OT_select_all_entities, VICHO_OT_deselect_all_entities
from ...vicho_operators import VICHO_OT_fake_op
from ..helper import YmapMixin

class VICHO_MT_entity_menu(bpy.types.Menu, YmapMixin):
    bl_label = "Entity Menu"
    bl_idname = "VICHO_MT_entity_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator(VICHO_OT_export_entity_asset.bl_idname, text="Export Asset(s)")
        layout.prop(self.get_ent(context), "is_mesh_edited", text="Mark as Edited")
        layout.separator()
        layout.menu(VICHO_MT_entity_select.bl_idname, text="Select")


class VICHO_MT_entity_select(bpy.types.Menu, YmapMixin):
    bl_label = "Select Entity"
    bl_idname = "VICHO_MT_entity_select"

    def draw(self, context):
        layout = self.layout
        layout.operator(VICHO_OT_select_all_entities.bl_idname, text="All")
        layout.operator(VICHO_OT_deselect_all_entities.bl_idname, text="None")
        layout.operator(VICHO_OT_invert_entity_selection.bl_idname, text="Invert")
        layout.menu(VICHO_MT_entity_select_by_type.bl_idname, text="By Type")

class VICHO_MT_entity_select_by_type(bpy.types.Menu, YmapMixin):
    bl_label = "Select by Type"
    bl_idname = "VICHO_MT_entity_select_by_type"

    def draw(self, context):
        layout = self.layout
        layout.operator(VICHO_OT_fake_op.bl_idname, text="Mark as Edited")
        layout.operator(VICHO_OT_fake_op.bl_idname, text="MLO Instance(s)")
        layout.operator(VICHO_OT_fake_op.bl_idname, text="Entity(s)")
        layout.operator(VICHO_OT_fake_op.bl_idname, text="No Linked Object")