import subprocess
import sys
import bpy
import os
import webbrowser

from .misc.funcs import export_milo_ymap_xml
from bpy.props import StringProperty
from bpy_extras.io_utils import ExportHelper
from .vicho_dependencies import dependencies_manager, is_dotnet_installed


class ContextSelectionRestrictedHelper:
    @classmethod
    def poll(cls, context):
        return context.active_object is not None


class ExportMLOTransFile(bpy.types.Operator, ContextSelectionRestrictedHelper):
    bl_idname = "vicho.exportmlostransformstofile"
    bl_label = "Export MLO transforms to YMAP"

    def execute(self, context):
        objs = context.selected_objects

        for obj in objs:
            if obj.sollum_type == "sollumz_bound_composite" or obj.type == "MESH":
                export_milo_ymap_xml(
                    "map1", obj, context.scene.ymap_instance_name_field
                )
                self.report(
                    {"INFO"}, f"{obj.name} location and rotation exported to file"
                )

            else:
                self.report(
                    {"WARNING"}, f"{obj.name} is not a Bound Composite or a Mesh"
                )

        return {"FINISHED"}


class PasteObjectTransformFromPickedObject(bpy.types.Operator):
    bl_idname = "vicho.pasteobjtransfrompickedobject"
    bl_label = "Set transforms"

    @classmethod
    def poll(cls, context):
        return context.scene.CopyDataFromObject is not None and (
            context.scene.locationOb_checkbox
            or context.scene.rotationOb_checkbox
            or context.scene.scaleOb_checkbox
        )

    def execute(self, context):
        from_obj = context.scene.CopyDataFromObject
        to_obj = context.scene.PasteDataToObject

        if context.scene.locationOb_checkbox:
            to_obj.location = from_obj.location
        if context.scene.rotationOb_checkbox:
            to_obj.rotation_euler = from_obj.rotation_euler
        if context.scene.scaleOb_checkbox:
            to_obj.scale = from_obj.scale

        return {"FINISHED"}


class MloYmapFileBrowser(bpy.types.Operator, ExportHelper):
    """Export MLO instance to YMAP"""

    bl_idname = "vicho.mloyampfilebrowser"
    bl_label = "Export MLO transforms to YMAP"
    bl_action = "Export a YMAP MLO"
    bl_showtime = True

    filename_ext = ".ymap"

    filter_glob: StringProperty(default="*.ymap", options={"HIDDEN"})

    def execute(self, context):
        try:
            export_milo_ymap_xml(
                self.filepath,
                context.active_object,
                context.scene.ymap_instance_name_field,
            )
            self.report({"INFO"}, f"{self.filepath} successfully exported")
            return {"FINISHED"}

        except Exception:
            self.report({"ERROR"}, f"Error exporting {self.filepath} ")
            return {"FINISHED"}


class DeleteAllColorAttributes(bpy.types.Operator, ContextSelectionRestrictedHelper):
    """Delete all color attributes from selected objects"""

    bl_idname = "vicho.deleteallcolorattributes"
    bl_label = "Color Attributes"

    def execute(self, context):
        objects = context.selected_objects
        removed_count = 0
        for obj in objects:
            if obj.type == "MESH":
                if obj.data.color_attributes:
                    removed_count = removed_count + 1
                    attrs = obj.data.color_attributes
                    for r in range(len(obj.data.color_attributes) - 1, -1, -1):
                        attrs.remove(attrs[r])
        return {"FINISHED"}


class DeleteAllVertexGroups(bpy.types.Operator, ContextSelectionRestrictedHelper):
    """Delete all vertex groups from selected objects"""

    bl_idname = "vicho.deleteallvertexgroups"
    bl_label = "Vertex Groups"

    def execute(self, context):
        objects = context.selected_objects

        for obj in objects:
            if obj.type == "MESH":
                for i in range(len(obj.vertex_groups)):
                    obj.vertex_groups.remove(obj.vertex_groups[0])
            else:
                continue

        return {"FINISHED"}


class DetectMeshesWithNoTextures(bpy.types.Operator, ContextSelectionRestrictedHelper):
    """Detect meshes with no textures in selected objects and then it print them in the console"""

    bl_idname = "vicho.detectmesheswithnotextures"
    bl_label = "Detect meshes with no textures"

    def execute(self, context):
        objects = context.selected_objects

        for obj in objects:
            if obj.type == "MESH":
                if len(obj.material_slots) < 1:
                    print(f"{obj.name} has no material slots")
                else:
                    for slot in obj.material_slots:
                        if slot.material.use_nodes:
                            if (
                                not slot.material.node_tree.nodes["Principled BSDF"]
                                .inputs["Base Color"]
                                .is_linked
                            ):
                                print(f"{obj.name} has no texture")

        return {"FINISHED"}


class RenameAllUvMaps(bpy.types.Operator, ContextSelectionRestrictedHelper):
    """Rename all UV maps from selected objects to Sollumz' standard"""

    bl_idname = "vicho.renamealluvmaps"
    bl_label = "UV Maps"

    def execute(self, context):
        objects = context.selected_objects
        for obj in objects:
            if obj.type == "MESH":
                for indx, uvmap in enumerate(obj.data.uv_layers):
                    uvmap.name = f"UVMap {indx}"

        return {"FINISHED"}


class VichoToolsInstallDependencies(bpy.types.Operator):
    bl_idname = "vicho.vichotoolsinstalldependencies"
    bl_label = "Install dependencies (Python.NET)"
    bl_description = "Install dependencies (Python.NET)"

    def execute(self, context):
        try:
            if not is_dotnet_installed():
                self.report(
                    {"ERROR"},
                    ".NET 8.0 or later is not installed. Please install it first.",
                )
                return {"CANCELLED"}

            try:
                import pythonnet

                self.report({"INFO"}, "Python.NET is already installed")
            except ImportError:
                self.report({"INFO"}, "Installing Python.NET...")
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "pythonnet"]
                )
                self.report({"INFO"}, "Python.NET installed successfully")

            if dependencies_manager.load_dependencies():
                self.report({"INFO"}, "Dependencies loaded successfully")
                print(f"dependencies.available: {dependencies_manager.available}")
                print(f"clr: {dependencies_manager.clr}")
                print(f"List: {dependencies_manager.List}")
                print(f"GameFiles: {dependencies_manager.GameFiles}")
                print(f"Utils: {dependencies_manager.Utils}")
            else:
                self.report({"ERROR"}, "Failed to load dependencies")
                return {"CANCELLED"}

            if dependencies_manager.available:
                self.report(
                    {"INFO"}, "All dependencies are now available and ready to use"
                )
            else:
                self.report(
                    {"ERROR"}, "Dependencies are still not available after loading"
                )
                return {"CANCELLED"}

        except subprocess.CalledProcessError as e:
            self.report({"ERROR"}, f"Error installing Python.NET: {str(e)}")
            return {"CANCELLED"}
        except Exception as e:
            self.report({"ERROR"}, f"Unexpected error: {str(e)}")
            return {"CANCELLED"}

        return {"FINISHED"}


class VichoToolsInstallDotnetRuntime(bpy.types.Operator):
    bl_idname = "vicho.vichotoolsinstalldotnetruntime"
    bl_label = "Install .NET 8 runtime"
    bl_description = "Install .NET 8 runtime"

    def execute(self, context):
        # download .NET 8 runtime from Microsoft
        try:
            webbrowser.open(
                "https://dotnet.microsoft.com/download/dotnet/thank-you/runtime-8.0.6-windows-x64-installer"
            )
            self.report({"INFO"}, "Download .NET 8 runtime from Microsoft's website")
        except:
            self.report(
                {"ERROR"},
                f"Error opening web browser to download .NET 8 runtime from Microsoft's website",
            )

        return {"FINISHED"}
