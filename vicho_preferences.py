import bpy
from .vicho_dependencies import dependencies_manager as d
from .vicho_operators import VICHO_OT_install_dotnet, VICHO_OT_import_strings
from .shared.helper import str_loaded_count, load_gta_cache
from .misc.helper import is_dotnet_installed
from .icons_load import get_icon

TAB_SETTINGS = (
    ("general", "General", "General settings for the addon", "SETTINGS", 0),
    ("dependencies", "Dependencies", "Manage addon dependencies", "SCRIPTPLUGINS", 1),
    ("texture_dictionary", "Texture(s)", "Settings for texture dictionary tools", "TEXTURE", 2),
    ("map_data", "Map Data", "Settings for map data tools", "IMAGE_DATA", 3),
    ("asset_import", "Asset Import", "Settings for asset import tools", "IMPORT", 4),
    ("about", "About", "Information about the addon", "INFO", 5),
)

authors = ["MrVicho13"]
members = ["(placeholder)"]

class VICHO_OT_load_game_files(bpy.types.Operator):
    """Load Game Files"""
    bl_idname = "assetimporter.load_game_files"
    bl_label = "Load GTA V Files"

    @classmethod
    def poll(cls, context):
        return get_addon_preferences().gta5_dir is not None and d.gamecache is None
    
    def execute(self, context):
        if load_gta_cache(get_addon_preferences().gta5_dir):
            self.report({"INFO"}, "Game files successfully loaded")
            context.scene.is_vicho_gta_loaded = True
        else:
            self.report({"ERROR"}, "Couldn't load game files, try again.")
        return {'FINISHED'}


class VichoToolsAddonProperties(bpy.types.AddonPreferences):
    bl_idname = __package__

    # General placeholders (fill in later)
    asset_database_dir: bpy.props.StringProperty(
        name="Asset Database Folder",
        subtype="DIR_PATH",
        description="(Placeholder) Folder used by asset database features",
        default="",
    )  # type: ignore

    strings_filepath: bpy.props.StringProperty(
        name="Strings File",
        subtype="FILE_PATH",
        description="(Placeholder) Default strings file to load",
        default="",
    )  # type: ignore

    add_nonsollumz_to_ytd: bpy.props.BoolProperty(
        name="Add Non-Sollumz objects in texture package(s)", default=False, description="Non-Sollumz objects will be able to be added to texture package(s) as long as they are meshes"
    )  # type: ignore
    enable_folder_export: bpy.props.BoolProperty(
        name="Enable folders export", default=False, description="If enabled, the export of folders will be available"
    )  # type: ignore
    
    skip_environment_textures: bpy.props.BoolProperty(
        name="Skip environment textures", default=True, description="If enabled, environment textures will be skipped"
    )  # type: ignore
    resize_dds: bpy.props.BoolProperty(
        name="Resize DDS textures", default=True, description="If enabled, DDS Textures will be affected by the resize settings"
    )  # type: ignore
    
    load_strings_on_startup: bpy.props.BoolProperty(
        name="Load strings on startup", default=False, description="If enabled, strings will be loaded on startup")  # type: ignore

    # Map data placeholders (fill in later)
    map_data_dir: bpy.props.StringProperty(
        name="Map Data Folder",
        subtype="DIR_PATH",
        description="(Placeholder) Folder for map data imports/exports",
        default="",
    )  # type: ignore

    # Asset import placeholders (fill in later)
    gta5_dir: bpy.props.StringProperty(
        name="Grand Theft Auto V Folder",
        subtype="DIR_PATH",
        description="Game Folder Location",
        default="",
    )  # type: ignore

    tab_settings: bpy.props.EnumProperty(
        name="Settings Tab",
        description="Select the settings tab to display",
        items=TAB_SETTINGS,
        default="general",
    )  # type: ignore
        
    def draw(self, context):
        layout = self.layout
        strings_loaded: int = str_loaded_count()

        tabs = layout.grid_flow(
            row_major=True,
            columns=len(TAB_SETTINGS),
            even_columns=True,
            even_rows=True,
            align=True,
        )
        tabs.use_property_decorate = False
        tabs.use_property_split = False
        tabs.prop(self, "tab_settings", expand=True)
        layout.separator(type="LINE")

        match self.tab_settings:
            case "general":
                col = layout.column(align=True)
                col.prop(self, "asset_database_dir", icon="FILE_FOLDER")
                col.prop(self, "strings_filepath", icon="FILE")
                col.prop(self, "load_strings_on_startup", icon="CHECKBOX_HLT")
                if strings_loaded is not None:
                    op = col.operator(
                        VICHO_OT_import_strings.bl_idname,
                        text=f"Load Strings ({str(strings_loaded)})",
                        icon="FILE_TICK",
                    )
                    op.load_on_startup = self.load_strings_on_startup

            case "texture_dictionary":
                col = layout.column(align=False)
                col.alignment = "CENTER"
                col.prop(self, "add_nonsollumz_to_ytd")
                col.prop(self, "enable_folder_export")
                col.prop(self, "skip_environment_textures")
                col.prop(self, "resize_dds")

            case "map_data":
                col = layout.column(align=True)
                col.prop(self, "map_data_dir", icon="FILE_FOLDER")
                col.label(text="(Placeholder) Map data settings go here.", icon="INFO")

            case "asset_import":
                col = layout.column(align=True)
                col.prop(self, "gta5_dir", icon="FILE_FOLDER")
                col.operator(VICHO_OT_load_game_files.bl_idname, icon="FILE_TICK")

            case "dependencies":
                col = layout.column(align=True)

                if not is_dotnet_installed():
                    col.operator(
                        VICHO_OT_install_dotnet.bl_idname,
                        text="Install .NET 9 runtime",
                        icon="SCRIPTPLUGINS",
                    )
                else:
                    col.label(text=".NET 9 x64 Runtime is already installed.")

                col.separator()

                if d.available:
                    col.label(text="Dependencies are loaded.")
                else:
                    col.label(
                        text="Dependencies aren't loaded (restart Blender after installing deps).",
                        icon="ERROR",
                    )

            case "about":
                row = layout.row(align=True)
                row.alignment = "CENTER"
                col = row.column(align=True)
                col.alignment = "CENTER"
                col.label(text="VichoTools", icon_value=get_icon("home"))

                row = layout.row(align=True)
                row.alignment = "CENTER"
                col = row.column(align=True)
                col.alignment = "CENTER"
                col.label(text="Requires Sollumz to work • Do not redistribute")

                row = layout.row(align=True)
                row.alignment = "CENTER"
                col = row.column(align=True)
                col.operator("wm.url_open", text="Project Page", icon="URL").url = "(placeholder)"
                col.operator("wm.url_open", text="Submit an Issue", icon="URL").url = "(placeholder)"

                layout.separator(type="LINE", factor=2.0)

                row = layout.row(align=True)
                row.alignment = "CENTER"
                col = row.column(align=True)
                col.alignment = "CENTER"
                col.label(text="Author(s)", icon="USER")
                for author in authors:
                    r = layout.row(align=True)
                    r.alignment = "CENTER"
                    c = r.column(align=True)
                    c.alignment = "CENTER"
                    c.label(text=author)

                layout.separator(type="LINE")

                row = layout.row(align=True)
                row.alignment = "CENTER"
                col = row.column(align=True)
                col.alignment = "CENTER"
                col.label(text="Members", icon="GROUP")
                for member in members:
                    r = layout.row(align=True)
                    r.alignment = "CENTER"
                    c = r.column(align=True)
                    c.alignment = "CENTER"
                    c.label(text=member)

                layout.separator(type="LINE", factor=2.0)
                row = layout.row(align=True)
                row.alignment = "CENTER"
                col = row.column(align=True)
                col.alignment = "CENTER"
                col.label(text="VichoTools (placeholder)", icon="HOME")
                col.separator()

def get_addon_preferences() -> VichoToolsAddonProperties:
    return bpy.context.preferences.addons[__package__].preferences

def register():
    bpy.utils.register_class(VichoToolsAddonProperties)

def unregister():
    bpy.utils.unregister_class(VichoToolsAddonProperties)
