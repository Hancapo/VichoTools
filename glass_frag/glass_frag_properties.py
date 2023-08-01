import bpy

class GlassFragList(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # Ajusta este valor para cambiar el espacio entre los elementos
            split = layout.split(factor=0.05)
            split.label(text=str(index))
            split.prop(item, "name", text="", emboss=False, icon='SELECT_SET')


class ProjectionGroup(bpy.types.PropertyGroup):
    T: bpy.props.FloatVectorProperty(
        name="Projection T", size=3, subtype='XYZ')
    U: bpy.props.FloatVectorProperty(
        name="Projection U", size=3, subtype='XYZ')
    V: bpy.props.FloatVectorProperty(
        name="Projection V", size=3, subtype='XYZ')


class GlassFragItem(bpy.types.PropertyGroup):
    projection: bpy.props.PointerProperty(type=ProjectionGroup)
    flags: bpy.props.IntProperty(name="Flags", default=768)
    unk_float_13: bpy.props.FloatProperty(name="UnkFloat13", default=0)
    unk_float_14: bpy.props.FloatProperty(name="UnkFloat14", default=0)
    unk_float_15: bpy.props.FloatProperty(name="UnkFloat15", default=1)
    unk_float_16: bpy.props.FloatProperty(name="UnkFloat16", default=1)
    thickness: bpy.props.FloatProperty(name="Thickness", default=0.005859375)
    unk_float_18: bpy.props.FloatProperty(
        name="UnkFloat18", default=0.0257826876)
    unk_float_19: bpy.props.FloatProperty(
        name="UnkFloat19", default=0.0142173115)
    tangent: bpy.props.FloatVectorProperty(
        name="Tangent", size=3, subtype='XYZ')
    layout_type: bpy.props.EnumProperty(
        name="Layout Type",
        items=[
            ('GTAV4', "GTAV4", "")
        ],
        default='GTAV4'
    )