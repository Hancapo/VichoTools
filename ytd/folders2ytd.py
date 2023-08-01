import bpy


class F2YTDGroup(bpy.types.PropertyGroup):
    bpy.types.Scene.mip_maps = bpy.props.BoolProperty(
        name="Generate Mip Maps",
        description="Generate Mip Maps for the textures",
        default=True)

    bpy.types.Scene.quality_mode = bpy.props.EnumProperty(
        name="Quality Mode",
        description="Quality Mode",
        items=[("fast", "Fast", "Process non-DDS with fast quality"),
               ("balanced", "Balanced", "Process non-DDS with balanced quality"),
               ("hq", "High Quality", "Process non-DDS with high quality")],
               default="balanced")
    bpy.types.Scene.transparency = bpy.props.BoolProperty(
        name="Detect Transparency",
        description="Detect Transparency",
        default = True)

    bpy.types.Scene.export_mode=bpy.props.EnumProperty(
        name = "Export Mode",
        description = "Export Mode",
        items = [("ytd", "YTD(s)", "Convert folders to YTD")])
