import bpy


class Vicho_TextureDictionaryPanel(bpy.types.Panel):
    bl_label = "Texture Dictionary Tools"
    bl_idname = "VICHO_PT_texture_dictionary"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Misc Tools"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text="", icon="TEXTURE")

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        list_col = row.column()
        scene = context.scene
        list_col.template_list("YtdList", "", scene,
                               "ytd_list", scene, "ytd_active_index")
        list_col.separator()
        row2 = list_col.row()
        row2.operator("ytd_list.add_ytd", icon='ADD',
                      text="Create Folder from selected object(s)")
        row2.operator("ytd_list.remove_ytd",
                      icon='REMOVE', text="Delete Folder")
        list_col.separator()
        row3 = list_col.row()
        row3.operator("ytd_list.reload_all", icon='FILE_REFRESH',
                      text="Reload all folders in list")
        row3.operator("ytd_list.add_to_ytd", icon='IMPORT',
                      text="Add selected object(s) to folder")
        list_col.separator()
        list_col.operator("ytd_list.assign_ytd_field_from_list",
                          icon='CURRENT_FILE', text="Auto-fill Texture Dictionary fields")
        list_col.separator()
        list_col.prop(scene, "ytd_export_path", text="Export path")
        list_col.separator()
        list_col.prop(scene, "convert_to_ytd",
                      text="Create YTD file(s) with Folder2YTD")
        if (scene.convert_to_ytd):
            list_col.separator()
            row4 = list_col.row()
            row4.prop(scene, "mip_maps", text="Generate MipMaps")
            row4.prop(scene, "quality_mode", text="Quality")
            row4.separator()
            row5 = list_col.row()
            row5.prop(scene, "transparency", text="Detect transparency")
            row5.prop(scene, "export_mode", text="Export mode")
        list_col.separator()
        list_col.operator("vicho.exportytdfolders",
                          text="Export list as Folders", icon='FILE_FOLDER')
        list_col.separator()
        list_col.operator("vicho.exportytdfiles",
                          text="Export list as YTD Files", icon='FORCE_TEXTURE')
