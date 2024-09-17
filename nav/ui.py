import bpy
from bpy.types import Context
from .operators import Import_YNV

class VichoNavmeshesTools_PT_Panel(bpy.types.Panel):
    bl_label = "Navmeshes"
    bl_idname = "VICHOTOOLS_PT_Navmeshes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vicho's Tools"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context: Context):
        self.layout.label(text="", icon="VIEW_PERSPECTIVE")
        
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        col = row.column()
        col.operator(Import_YNV.bl_idname, text="Import YNV(s)", icon="IMPORT")



class VichoTypeObject_PT_Panel(bpy.types.Panel):
    bl_label = "Vicho's Tools"
    bl_idname = "VICHOTOOLS_PT_VichoTypeObject"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = row.column()
        col.prop(context.object, "vicho_type")
        col.separator()
        
        if context.object.vicho_type == "vicho_nav_mesh":
            col.prop(context.object.navmesh_properties, "AreaID")
            col.prop(context.object.navmesh_properties, "UnkHash")
            box = col.box()
            box.label(text="Content Flags")
            row = box.row()
            col = row.column()
            col.prop(context.object.navmesh_properties.ContentFlags, "Polygons")
            col.prop(context.object.navmesh_properties.ContentFlags, "Portals")
            col.prop(context.object.navmesh_properties.ContentFlags, "Vehicle")
            col.prop(context.object.navmesh_properties.ContentFlags, "Unknown8")
            col.prop(context.object.navmesh_properties.ContentFlags, "Unknown16")
        if context.object.vicho_type == "vicho_nav_point":
            col.prop(context.object.navpoint_properties, "Type")