import bpy

from ..vicho_dependencies import depen_installed

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

        if(len(scene.ytd_list) > 0):
            list_col.separator()
            list_col.operator("ytd_list.assign_ytd_field_from_list", icon='CURRENT_FILE', text="Auto-fill Texture Dictionary fields")
            list_col.separator()
            list_col.prop(scene, "ytd_export_path", text="Export path")
            list_col.separator()
            
            # Export options

            if depen_installed:
                list_col.prop(scene, "convert_to_ytd", text="Create YTD file(s)")
            else:
                list_col.label(text="YTD(s) Export disabled since dependencies not installed, check add-on's properties", icon="ERROR")
            if scene.convert_to_ytd:
                row5 = list_col.row(align=True)
                #row5.prop(scene, "transparency", text="Detect transparency")
                list_col.separator()
                list_col.operator("vicho.exportytdfiles", text="Export list as YTD Files", icon='FORCE_TEXTURE')
            
            # Final export options
            list_col.separator()
            list_col.operator("vicho.exportytdfolders", text="Export list as Folders", icon='FILE_FOLDER')
