import bpy
from .vicho_dependencies import is_dotnet_installed, dependencies_manager as d
from .vicho_operators import VichoToolsInstallDependencies, VichoToolsInstallDotnetRuntime

class VichoToolsAddonProperties(bpy.types.AddonPreferences):
    bl_idname = __package__
    add_nonsollumz_to_ytd: bpy.props.BoolProperty(
        name="Add Non-Sollumz objects in YTD/Texture folder(s)", default=False, description="Non-Sollumz objects will be able to be added to YTD/Texture folder(s) as long as they are meshes."
    )
    enable_folder_export: bpy.props.BoolProperty(
        name="Enable folders export", default=False, description="If enabled, the export of folders will be available."
    )

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        if not is_dotnet_installed():
             col.operator(VichoToolsInstallDotnetRuntime.bl_idname, text="Install first: .NET 8 runtime", icon="SCRIPTPLUGINS")
        else:
            col.label(text=".NET 8 x64 Runtime is already installed.")
        col.separator()
        if d.available:
            col.label(text="PythonNET is already installed.")
        else:
            col.operator(VichoToolsInstallDependencies.bl_idname, text="Install second: Install PythonNET", icon="SCRIPTPLUGINS")
        col.separator()
        box = col.box()
        col = box.column(align=True)
        col.label(text="Texture(s) Settings", icon="TEXTURE")
        col.separator()
        col.prop(self, "add_nonsollumz_to_ytd")
        col.separator()
        col.prop(self, "enable_folder_export")


def get_addon_preferences() -> VichoToolsAddonProperties:
    return bpy.context.preferences.addons[__package__].preferences


def register():
    bpy.utils.register_class(VichoToolsAddonProperties)

def unregister():
    bpy.utils.unregister_class(VichoToolsAddonProperties)