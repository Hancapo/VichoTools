import bpy
from .vicho_dependencies import depen_installed, is_dotnet_installed
from .vicho_operators import VichoToolsInstallDependencies, VichoToolsInstallDotnetRuntime

class VichoToolsAddonProperties(bpy.types.AddonPreferences):
    bl_idname = __package__.split(".")[0]
    add_nonsollumz_to_ytd: bpy.props.BoolProperty(
        name="Add Non-Sollumz objects in YTD/Texture folder(s)", default=False, description="Non-Sollumz objects will be able to be added to YTD/Texture folder(s) as long as they are meshes."
    )
    enable_folder_export: bpy.props.BoolProperty(
        name="Enable folders export", default=False, description="If enabled, the export of folders will be available."
    )

    def draw(self, context):
        layout = self.layout
        if not is_dotnet_installed():
             layout.label(text=".NET 8 x64 runtime is not installed.", icon="APPEND_BLEND")
             layout.operator(VichoToolsInstallDotnetRuntime.bl_idname, text="Install first: .NET 8 runtime", icon="SCRIPTPLUGINS")
        else:
            layout.label(text=".NET 8 x64 Runtime is already installed.")
             
        if not depen_installed():
                layout.operator(VichoToolsInstallDependencies.bl_idname, text="Install second: Install PythonNET", icon="SCRIPTPLUGINS")
        else:
            layout.label(text="PythonNET is already installed.")
        layout.prop(self, "add_nonsollumz_to_ytd")
        layout.prop(self, "enable_folder_export")


def get_addon_preferences(context: bpy.types.Context) -> VichoToolsAddonProperties:
    return context.preferences.addons[__package__.split(".")[0]].preferences
    