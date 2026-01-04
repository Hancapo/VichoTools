import bpy
from ..operators.operators_entity import VICHO_OT_export_entity_asset

class VICHO_MT_entity_menu(bpy.types.Menu):
    bl_label = "Entity Menu"
    bl_idname = "VICHO_MT_entity_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator(VICHO_OT_export_entity_asset.bl_idname, text="Export Asset")