import bpy


class VichoToolsAddonProperties(bpy.types.AddonPreferences):
    bl_idname = __package__.split(".")[0]

    folders2ytd_path: bpy.props.StringProperty(
        name="Folder2YTD path", subtype='DIR_PATH' )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "folders2ytd_path")
        self.folders2ytd_path = bpy.path.abspath(self.folders2ytd_path)


def get_addon_preferences(context: bpy.types.Context) -> VichoToolsAddonProperties:
    return context.preferences.addons[__package__.split(".")[0]].preferences
