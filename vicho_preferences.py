import bpy
from .vicho_dependencies import is_dotnet_installed, dependencies_manager as d
from .vicho_operators import VICHO_OT_install_dotnet, VICHO_OT_import_strings
from .ymap.helper import str_loaded_count

class VichoToolsAddonProperties(bpy.types.AddonPreferences):
    bl_idname = __package__
    add_nonsollumz_to_ytd: bpy.props.BoolProperty(
        name="Add Non-Sollumz objects in texture package(s)", default=False, description="Non-Sollumz objects will be able to be added to texture package(s) as long as they are meshes"
    )
    enable_folder_export: bpy.props.BoolProperty(
        name="Enable folders export", default=False, description="If enabled, the export of folders will be available"
    )
    
    skip_environment_textures: bpy.props.BoolProperty(
        name="Skip environment textures", default=True, description="If enabled, environment textures will be skipped"
    )
    resize_dds: bpy.props.BoolProperty(
        name="Resize DDS textures", default=True, description="If enabled, DDS Textures will be affected by the resize settings"
    )
    
    load_strings_on_startup: bpy.props.BoolProperty(
        name="Load strings on startup", default=False, description="If enabled, strings will be loaded on startup")
        
    def draw(self, context):
        layout = self.layout
        strings_loaded: int = str_loaded_count()
        col = layout.column(align=True)
        col.label(text="Dependencies", icon="SETTINGS")
        col.separator()
        if not is_dotnet_installed():
            col.operator(VICHO_OT_install_dotnet.bl_idname, text="Install first: .NET 9 runtime", icon="SCRIPTPLUGINS")
        else:
            col.label(text=".NET 9 x64 Runtime is already installed.")
        col.separator()
        if d.available:
            col.label(text="PythonNET is already available.")
        else:
            col.label(text="No need to install PythonNET, it's already included in wheels, you shouldn't be seeing this, report it as soon as possible.")
        header, panel = layout.panel("texture_settings", default_closed=False)
        header.label(text= "Texture(s) Settings", icon="TEXTURE")
        if panel:
            panel_col = panel.column(align=True)
            panel_col.prop(self, "add_nonsollumz_to_ytd", icon="STICKY_UVS_LOC")
            panel_col.prop(self, "enable_folder_export", icon="NEWFOLDER")
            panel_col.prop(self, "skip_environment_textures", icon="SHADING_RENDERED")
            panel_col.prop(self, "resize_dds", icon="UV_DATA")
        col.separator()
        header, panel = layout.panel("general_settings", default_closed=False)
        header.label(text="General Settings", icon="INFO")
        if panel:
            panel_col = panel.column(align=True)
            if strings_loaded is not None:
                panel_col.operator(VICHO_OT_import_strings.bl_idname, text=f"Load Strings ({str(strings_loaded)})", icon="FILE_TICK")

def get_addon_preferences() -> VichoToolsAddonProperties:
    return bpy.context.preferences.addons[__package__].preferences

def register():
    bpy.utils.register_class(VichoToolsAddonProperties)

def unregister():
    bpy.utils.unregister_class(VichoToolsAddonProperties)