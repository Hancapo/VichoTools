import bpy


class VichoFragmentToolsPanel(bpy.types.Panel):
    bl_label = "Fragment Tools"
    bl_idname = "VICHOFRAGMENTTOOLS_PT_"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Misc Tools"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text="", icon="AUTO")

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Warning row
        row = layout.row()
        row.label(
            text="WARNING: This tool will be useless as soon as the newest Sollumz update comes out!", icon='ERROR')

        # Operator row
        row = layout.row()
        row.operator("vicho.createfragchildsfromcols",
                     icon="CON_CHILDOF")

        # Material density row
        row = layout.row()
        row.prop(scene, "material_density", text="Material")

        # Separator
        layout.separator()

        # Bone Tags label
        row = layout.row()
        row.label(text="Bone Tags", icon='BONE_DATA')

        # Three columns in a row
        row = layout.row(align=True)
        col1 = row.column(align=True)
        col1.prop(scene, "fragbonetag_transx", text="TransX")
        col1.prop(scene, "fragbonetag_transy", text="TransY")
        col1.prop(scene, "fragbonetag_transz", text="TransZ")

        col2 = row.column(align=True)
        col2.prop(scene, "fragbonetag_rotx", text="RotX")
        col2.prop(scene, "fragbonetag_roty", text="RotY")
        col2.prop(scene, "fragbonetag_rotz", text="RotZ")

        col3 = row.column(align=True)
        col3.prop(scene, "fragbonetag_scalex", text="ScaleX")
        col3.prop(scene, "fragbonetag_scaley", text="ScaleY")
        col3.prop(scene, "fragbonetag_scalez", text="ScaleZ")

        # Separator
        layout.separator()
        # add button to create bone tags
        row = layout.row()
        row.operator("vicho.boneflagstoselectedbones", icon="CONSTRAINT_BONE")


class VichoCreateFragmentObjectsPanel(bpy.types.Panel):

    bl_label = "Create Fragment Objects"
    bl_idname = "VICHOFRAGMENTTOOLS_PT_CREATEFRAGMENTS"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Misc Tools"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = VichoFragmentToolsPanel.bl_idname

    def draw_header(self, context):
        self.layout.label(text="", icon="CUBE")

    def draw(self, context):

        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.operator("vicho.createarmaturefromselection", icon="OUTLINER_OB_ARMATURE")
        row.prop(scene, "yft_type", text="YFT Type")

        grid = layout.grid_flow(columns=3, even_columns=True, even_rows=True)
        grid.prop(scene, "create_multiple_yft", text="Separate Objects")

        grid.prop(scene, "bone_id_gen", text="Initial Bone ID")
