import bpy
class VichoGroup(bpy.types.PropertyGroup):
    bpy.types.Scene.file_name_field = bpy.props.StringProperty(
        name="File Name",
        default="",
        description="File name for the text file",
        maxlen=50,
    )
    bpy.types.Scene.CopyDataFromObject = bpy.props.PointerProperty(
        name="Target Object", type=bpy.types.Object
    )
    bpy.types.Scene.PasteDataToObject = bpy.props.PointerProperty(
        name="Source Object", type=bpy.types.Object
    )

    bpy.types.Scene.locationOb_checkbox = bpy.props.BoolProperty(
        name="Location", description="Location"
    )
    bpy.types.Scene.rotationOb_checkbox = bpy.props.BoolProperty(
        name="Rotation", description="Rotation"
    )
    bpy.types.Scene.scaleOb_checkbox = bpy.props.BoolProperty(
        name="Scale", description="Scale"
    )

