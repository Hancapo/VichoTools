import bpy

def update_path(self, context):
    self.ytd_export_path = bpy.path.abspath(self.ytd_export_path)

class VichoGroup(bpy.types.PropertyGroup):
    bpy.types.Scene.file_name_field = bpy.props.StringProperty(
        name="File Name",
        default="",
        description="File name for the text file",
        maxlen=50)

    bpy.types.Scene.ymap_instance_name_field = bpy.props.StringProperty(
        name="Instance Name",
        default="",
        description="instance name for the MLO Instance",
        maxlen=50)
    bpy.types.Scene.location_checkbox = bpy.props.BoolProperty(
        name="Reset Location",
        description="Reset location")
    bpy.types.Scene.rotation_checkbox = bpy.props.BoolProperty(
        name="Reset Rotation",
        description="Reset rotation")
    bpy.types.Scene.scale_checkbox = bpy.props.BoolProperty(
        name="Reset Scale",
        description="Reset scale")
    bpy.types.Scene.CopyDataFromObject = bpy.props.PointerProperty(
        name="Copy Data From Object",
        type=bpy.types.Object)
    bpy.types.Scene.PasteDataToObject = bpy.props.PointerProperty(
        name="Paste Data To Object",
        type=bpy.types.Object)

    bpy.types.Scene.locationOb_checkbox = bpy.props.BoolProperty(
        name="Location",
        description="Location")
    bpy.types.Scene.rotationOb_checkbox = bpy.props.BoolProperty(
        name="Rotation",
        description="Rotation")
    bpy.types.Scene.scaleOb_checkbox = bpy.props.BoolProperty(
        name="Scale",
        description="Scale")

    bpy.types.Scene.ytd_export_path = bpy.props.StringProperty(
        name="YTD Export Path",
        default="",
        description="Path to export the YTD file",
        subtype='DIR_PATH',
        update=update_path,
    )

    bpy.types.Scene.ytd_enum_process_type = bpy.props.EnumProperty(
        items=[('ALL', 'All', 'All the list'),
               ('CHECKED', 'All checked items', 'All the checked items'),
               ('SELECTED', 'Selected item', 'The selected item')],
        name="Process Type",
        default='ALL',
        description="Sets the type of export to perform over the list of texture dictionaries",
    )