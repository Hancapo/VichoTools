import bpy
import xml.etree.ElementTree as ET
from xml.dom import minidom
from .glass_frag_helper import add_glass_window_to_list


class GLASSLIST_OT_add(bpy.types.Operator):
    """Add a new glass window to the list"""
    bl_idname = "glass_frag_list.add_glass"
    bl_label = "Add a new glass window"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (
            context.mode == 'EDIT_MESH' and
            obj is not None and
            obj.type == 'MESH'
        )

    def execute(self, context):
        scene = context.scene
        glass_list = scene.glass_frag_list
        obj = context.selected_objects[0]
        if not (add_glass_window_to_list(glass_list, obj, self)):
            self.report({'ERROR'}, f"Failed to add a new glass window")
        else:
            self.report({'INFO'}, f"Added a new glass window")
        return {'FINISHED'}


class GLASSLIST_OT_remove(bpy.types.Operator):
    """Remove the selected glass window from the list"""
    bl_idname = "glass_frag_list.remove_glass"
    bl_label = "Remove glass window"

    @classmethod
    def poll(cls, context):
        scene = context.scene
        return scene.glass_frag_list and scene.glass_frag_active_index >= 0

    def execute(self, context):
        scene = context.scene
        glass_list = scene.glass_frag_list
        glass_list_index = scene.glass_frag_active_index

        if glass_list_index < len(glass_list):
            glass_list.remove(glass_list_index)
            scene.glass_frag_active_index = min(
                max(0, glass_list_index - 1), len(glass_list) - 1)
            self.report({'INFO'}, "Removed glass window")
        else:
            self.report({'ERROR'}, "Failed to remove glass window")
        return {'FINISHED'}


class GLASSLIST_OT_export_xml(bpy.types.Operator):
    """Export all glass windows to XML"""
    bl_idname = "glass_frag_list.export_xml"
    bl_label = "Export to XML"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        scene = context.scene
        return len(scene.glass_frag_list) > 0

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        scene = context.scene
        glass_list = scene.glass_frag_list

        root = ET.Element("GlassWindows")

        

        for item in glass_list:
            item_elem = ET.SubElement(root, "Item")

            ET.SubElement(item_elem, "Flags", {"value": str(item.flags)})

            projection_elem = ET.SubElement(item_elem, "Projection\n")
            projection_elem.text = f"\n     {round(item.projection.T[0], 6)} {round(item.projection.T[1], 6)} {round(item.projection.T[2], 6)}"
            projection_elem.text += f"\n     {round(item.projection.U[0], 6)} {round(item.projection.U[1], 6)} {round(item.projection.U[2], 6)}"
            projection_elem.text += f"\n     {round(item.projection.V[0], 6)} {round(item.projection.V[1], 6)} {round(item.projection.V[2], 6)}\n    "

            ET.SubElement(item_elem, "UnkFloat13", {
                          "value": str(item.unk_float_13)})
            ET.SubElement(item_elem, "UnkFloat14", {
                          "value": str(item.unk_float_14)})
            ET.SubElement(item_elem, "UnkFloat15", {
                          "value": str(item.unk_float_15)})
            ET.SubElement(item_elem, "UnkFloat16", {
                          "value": str(item.unk_float_16)})
            ET.SubElement(item_elem, "Thickness", {
                          "value": str(item.thickness)})
            ET.SubElement(item_elem, "UnkFloat18", {
                          "value": str(item.unk_float_18)})
            ET.SubElement(item_elem, "UnkFloat19", {
                          "value": str(item.unk_float_19)})

            ET.SubElement(item_elem, "Tangent", {"x": str(
                round(item.tangent[0], 2)), "y": str(round(item.tangent[1], 2)), "z": str(round(item.tangent[2], 2))})

            layout_elem = ET.SubElement(item_elem, "Layout")
            layout_elem.set("type", item.layout_type)
            ET.SubElement(layout_elem, "Position")
            ET.SubElement(layout_elem, "Normal")
            ET.SubElement(layout_elem, "Colour0")
            ET.SubElement(layout_elem, "TexCoord0")
            ET.SubElement(layout_elem, "TexCoord1")

        xml_string = minidom.parseString(
            ET.tostring(root)).toprettyxml(indent="  ")

        with open(self.filepath, 'w') as f:
            f.write(xml_string)

        return {'FINISHED'}
