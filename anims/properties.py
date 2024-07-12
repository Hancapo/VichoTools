import bpy

class AnimProps(bpy.types.PropertyGroup):
    bpy.types.Scene.ycd_name = bpy.props.StringProperty(
        name="YCD Name",
        default="",
        description="Sets the name of the created clip dictionary",
        maxlen=60)
    bpy.types.Scene.autofill_clipdict = bpy.props.BoolProperty(
        name="Autofill Clip Dictionary",
        default=False,
        description="Autofills the clipDictionary field with the name of the clip dictionary if the selected objects were added to an YTYP"
    )
    bpy.types.Scene.calculate_anim_flags = bpy.props.BoolProperty(
        name="Calculate Animation Flags",
        default=False,
        description="Calculates the animation flags for the selected objects and then applies in objects' YTYP"
    )
    bpy.types.Scene.auto_start_anim_flag = bpy.props.BoolProperty(
        name="Auto Start Animation Flag",
        default=False,
        description="Sets the auto start flag for the selected objects and then applies in objects' YTYP"
    )