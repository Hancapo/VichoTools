import bpy
from .vicho_operators import (MloYmapFileBrowser, 
                              PasteObjectTransformFromPickedObject, 
                              DeleteAllColorAttributes, 
                              DeleteAllVertexGroups, 
                              DetectMeshesWithNoTextures, 
                              RenameAllUvMaps)

class VichoMloTools_PT_Panel(bpy.types.Panel):
    bl_label = "MLO"
    bl_idname = "VICHOTOOLS_PT_Mlo"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vicho's Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text="", icon="HOME")

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "ymap_instance_name_field", text="Instance name")
        row = layout.row()
        row.operator(MloYmapFileBrowser.bl_idname)


class VichoObjectTools_PT_Panel(bpy.types.Panel):
    bl_label = "Objects"
    bl_idname = "VICHOTOOLS_PT_Object"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vicho's Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text="", icon="OVERLAY")

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        # Section 2: Set Object Transforms to Picked Object
        col.separator()
        col.label(
            text="Set Object Transforms to Picked Object", icon="TRACKING_BACKWARDS"
        )

        row = col.row(align=True)
        row.prop(context.scene, "PasteDataToObject", text="From")
        row.prop(context.scene, "CopyDataFromObject", text="To")

        row = col.row(align=True)
        row.prop(context.scene, "locationOb_checkbox", text="Location")
        row.prop(context.scene, "rotationOb_checkbox", text="Rotation")
        row.prop(context.scene, "scaleOb_checkbox", text="Scale")

        col.operator(PasteObjectTransformFromPickedObject.bl_idname)

        # Section 3: Delete Meshes Without Data
        col.separator()
        col.label(text="Delete Meshes Without Data and Others", icon="DOT")
        col.separator()

        # Section 4: Delete All Color Attributes
        col.operator(DeleteAllColorAttributes.bl_idname)
        col.separator()

        # Section 5: Delete All Vertex Groups
        col.operator(DeleteAllVertexGroups.bl_idname)
        col.separator()

        col.operator(DetectMeshesWithNoTextures.bl_idname)
        col.separator()

        col.operator(RenameAllUvMaps.bl_idname)
        col.separator()
