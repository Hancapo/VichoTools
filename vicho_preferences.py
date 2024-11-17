import bpy
from .vicho_dependencies import is_dotnet_installed, dependencies_manager as d
from .vicho_operators import VICHO_OT_install_depens, VICHO_OT_install_dotnet

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
        
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        box_col = col.box()
        box_col.label(text="Dependencies", icon="SETTINGS")
        if not is_dotnet_installed():
             box_col.operator(VICHO_OT_install_dotnet.bl_idname, text="Install first: .NET 8 runtime", icon="SCRIPTPLUGINS")
        else:
            box_col.label(text=".NET 8 x64 Runtime is already installed.")
        if d.available:
            box_col.label(text="PythonNET is already installed.")
        else:
            box_col.operator(VICHO_OT_install_depens.bl_idname, text="Install second: Install PythonNET", icon="SCRIPTPLUGINS")
        col.separator()
        box = col.box()
        col = box.column(align=True)
        col.label(text="Texture(s) Settings", icon="TEXTURE")
        col.separator()
        col.prop(self, "add_nonsollumz_to_ytd", icon="STICKY_UVS_LOC")
        col.prop(self, "enable_folder_export", icon="NEWFOLDER")
        col.prop(self, "skip_environment_textures", icon="SHADING_RENDERED")
        col.prop(self, "resize_dds", icon="UV_DATA")
        

def get_addon_preferences() -> VichoToolsAddonProperties:
    return bpy.context.preferences.addons[__package__].preferences


def register():
    bpy.utils.register_class(VichoToolsAddonProperties)

def unregister():
    bpy.utils.unregister_class(VichoToolsAddonProperties)