import bpy
from .vicho_dependencies import depen_installed
from .vicho_operators import VichoToolsInstallDependencies

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
        layout.label(text=".NET 8 x64 Runtime MUST BE installed.", icon="APPEND_BLEND")
        if not depen_installed():
                layout.operator(VichoToolsInstallDependencies.bl_idname, text="Install PythonNET", icon="SCRIPTPLUGINS")
        else:
            layout.label(text="PythonNET is already installed.")
        layout.prop(self, "add_nonsollumz_to_ytd")
        layout.prop(self, "enable_folder_export")


def get_addon_preferences(context: bpy.types.Context) -> VichoToolsAddonProperties:
    return context.preferences.addons[__package__.split(".")[0]].preferences
    