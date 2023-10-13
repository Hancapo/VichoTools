import bpy
from .vicho_dependencies import depen_installed, is_imagemagick_installed
from .vicho_operators import VichoToolsInstallDependencies, VichoToolsMagickInstallCheck

class VichoToolsAddonProperties(bpy.types.AddonPreferences):
    bl_idname = __package__.split(".")[0]
    add_nonsollumz_to_ytd: bpy.props.BoolProperty(
        name="Enable the inclusion of non-Sollumz objects in YTD/Texture folder(s)", default=False, description="If enabled, non-Sollumz objects can be added to YTD/Texture folder(s) as long as they are meshes."
    )

    def draw(self, context):
        layout = self.layout

        if not is_imagemagick_installed():
            layout.operator(VichoToolsMagickInstallCheck.bl_idname, text="1. Install ImageMagick", icon="SCRIPTPLUGINS")
        else:
            layout.label(text="ImageMagick is already installed.")
        if not depen_installed():
            layout.operator(VichoToolsInstallDependencies.bl_idname, text="2. Install PythonNET and Wand", icon="SCRIPTPLUGINS")
        else:
            layout.label(text="PythonNET and Wand are already installed.")
        layout.prop(self, "add_nonsollumz_to_ytd")


def get_addon_preferences(context: bpy.types.Context) -> VichoToolsAddonProperties:
    return context.preferences.addons[__package__.split(".")[0]].preferences
