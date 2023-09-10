import bpy


class VichoToolsAddonProperties(bpy.types.AddonPreferences):
    bl_idname = __package__.split(".")[0]

    folders2ytd_path: bpy.props.StringProperty(
        name="Folder2YTD path", subtype='DIR_PATH', description="Path to Folder2YTD.exe")
    add_nonsollumz_to_ytd: bpy.props.BoolProperty(
        name="Enable the inclusion of non-Sollumz objects in YTD/Texture folder(s)", default=False, description="If enabled, non-Sollumz objects can be added to YTD/Texture folder(s) as long as they are meshes."
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "folders2ytd_path")
        layout.separator()
        layout.prop(self, "add_nonsollumz_to_ytd")


def get_addon_preferences(context: bpy.types.Context) -> VichoToolsAddonProperties:
    return context.preferences.addons[__package__.split(".")[0]].preferences
