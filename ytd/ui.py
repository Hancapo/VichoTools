import bpy

from ..vicho_dependencies import depen_installed

class Vicho_TextureDictionaryPanel(bpy.types.Panel):
    bl_label = "Texture Dictionary Tools"
    bl_idname = "VICHO_PT_texture_dictionary"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vicho's Tools"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw_header(self, context):
        self.layout.label(text="", icon="TEXTURE")

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if(depen_installed()):
            row = layout.row()
            col = row.column(align=True)
            col.separator(factor=3.5)
            col.operator("ytd_list.add_ytd", text="", icon="ADD")
            col.operator("ytd_list.remove_ytd", text="", icon="REMOVE")
            col.separator()
            col.operator("ytd_list.reload_all", text="", icon="FILE_REFRESH")
            col.operator("ytd_list.add_to_ytd", text="", icon="IMPORT")
            col.separator()
            col.operator("ytd_list.assign_ytd_field_from_list", text="", icon="CURRENT_FILE")

            row = row.row()
            col = row.column(align=True)
            col.label(text="Texture Dictionaries", icon="TEXTURE")
            col.template_list ("YTDLIST_UL_list", "", scene, "ytd_list", scene, "ytd_active_index")
            row = row.row()
            col = row.column(align=True)
            col.label(text="Meshes", icon="MESH_DATA")
            col.template_list ("MESHLIST_UL_list", "", scene, "mesh_list", scene, "mesh_active_index")
            row = row.row()
            col = row.column(align=True)
            col.separator(factor=3.5)
            col.operator("ytd_list.select_meshes_from_ytd_folder", text="", icon="RESTRICT_SELECT_OFF")
            col.operator("mesh_list.delete_mesh", text="", icon="X")
            
            col = layout.column(align=True)
            col.separator()
            row = col.row(align=True)
            row.prop(scene, "ytd_show_explorer_after_export", text='Show containing folder after export', icon='FOLDER_REDIRECT')
            row.prop(scene, "ytd_export_path", text="")
            col.separator()
            row = col.row(align=True)
            col.prop(scene, "ytd_enum_process_type", text="")
            

            col = layout.column(align=True)
            col.separator()

            col = col.row(align=True)
            col.operator("vicho.exportytdfiles", text="As YTD File(s)", icon='FORCE_TEXTURE')
            col.operator("vicho.exportytdfolders", text="As Folder(s)", icon='FILE_FOLDER')
        else:
            layout.label(text="Dependencies not installed, please make sure you check the Add-on's preference menu", icon="ERROR")
        
