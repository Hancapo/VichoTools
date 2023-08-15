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
        scene = context.scene
        
        # List of items
        row = layout.row()
        list_col = row.column()
        list_col.template_list("YtdList", "", scene, "ytd_list", scene, "ytd_active_index")
        
        # Item operations
        row2 = list_col.row(align=True)
        row2.operator("ytd_list.add_ytd", icon='ADD', text="Create Folder from selected object(s)")
        row2.operator("ytd_list.remove_ytd", icon='REMOVE', text="Delete Folder")
        
        # List operations
        row3 = list_col.row(align=True)
        row3.operator("ytd_list.reload_all", icon='FILE_REFRESH', text="Reload all folders in list")
        row3.operator("ytd_list.add_to_ytd", icon='IMPORT', text="Add selected object(s) to folder")
        
        # Auto-fill and export options
        list_col.separator()
        list_col.operator("ytd_list.assign_ytd_field_from_list", icon='CURRENT_FILE', text="Auto-fill Texture Dictionary fields")
        list_col.separator()
        list_col.prop(scene, "ytd_export_path", text="Export path")
        list_col.separator()
        
        # Export options
        list_col.prop(scene, "convert_to_ytd", text="Create YTD file(s) with Folder2YTD")
        if scene.convert_to_ytd:
            list_col.separator()
            list_col.label(text="Warning: This feature is experimental. Run Blender as Administrator if needed.", icon='ERROR')
            row4 = list_col.row(align=True)
            row4.prop(scene, "mip_maps", text="Generate MipMaps")
            row4.prop(scene, "quality_mode", text="Quality")
            
            row5 = list_col.row(align=True)
            row5.prop(scene, "transparency", text="Detect transparency")
            row5.prop(scene, "export_mode", text="Export mode")
            
            list_col.separator()
            list_col.operator("vicho.exportytdfiles", text="Export list as YTD Files", icon='FORCE_TEXTURE')
        
        # Final export options
        list_col.separator()
        list_col.operator("vicho.exportytdfolders", text="Export list as Folders", icon='FILE_FOLDER')
