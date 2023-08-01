import bpy


class MaterialDensityPropertyEnum(bpy.types.PropertyGroup):
    bpy.types.Scene.material_density = bpy.props.EnumProperty(
        name="Material Density",
        items=[(str(1000), "Water", "Sets density to Water"),
               (str(1.2), "Air", "Sets density to Air"),
               (str(7870), "Iron", "Sets density to Iron"),
               (str(2700), "Aluminum", "Sets density to Aluminum"),
               (str(8960), "Copper", "Sets density to Copper"),
               (str(11340), "Lead", "Sets density to Lead"),
               (str(19320), "Gold", "Sets density to Gold"),
               (str(10490), "Silver", "Sets density to Silver"),
               (str(2500), "Glass", "Sets density to Glass"),
               (str(710), "Wood", "Sets density to Wood"),
               (str(2260), "Titanium", "Sets density to Titanium"),
               (str(7800), "Nickel", "Sets density to Nickel"),
               (str(8480), "Steel", "Sets density to Steel"),
               (str(2330), "Alloy 20", "Sets density to Alloy 20"),
               (str(2700), "Brass", "Sets density to Brass"),
               (str(8050), "Zinc", "Sets density to Zinc"),
               (str(8900), "Tungsten", "Sets density to Tungsten"),
               (str(2100), "Beryllium", "Sets density to Beryllium"),
               (str(4400), "Platinum", "Sets density to Platinum"),
               ]
    )


class FragmentBoneTagsGroup(bpy.types.PropertyGroup):
    bpy.types.Scene.fragbonetag_transx = bpy.props.BoolProperty(
        name="TransX", default=False)
    bpy.types.Scene.fragbonetag_transy = bpy.props.BoolProperty(
        name="TransY", default=False)
    bpy.types.Scene.fragbonetag_transz = bpy.props.BoolProperty(
        name="TransZ", default=False)
    bpy.types.Scene.fragbonetag_rotx = bpy.props.BoolProperty(
        name="RotX", default=False)
    bpy.types.Scene.fragbonetag_roty = bpy.props.BoolProperty(
        name="RotY", default=False)
    bpy.types.Scene.fragbonetag_rotz = bpy.props.BoolProperty(
        name="RotZ", default=False)
    bpy.types.Scene.fragbonetag_scalex = bpy.props.BoolProperty(
        name="ScaleX", default=False)
    bpy.types.Scene.fragbonetag_scaley = bpy.props.BoolProperty(
        name="ScaleY", default=False)
    bpy.types.Scene.fragbonetag_scalez = bpy.props.BoolProperty(
        name="ScaleZ", default=False)


class VichoFragmentCreationToolsProperties(bpy.types.PropertyGroup):
    bpy.types.Scene.yft_type = bpy.props.EnumProperty(
        name="Type",
        items=[("glass_windows", "Glass Window(s)", "To create glass windows"),
                ("dynamic_object", "Dynamic Object(s)", "To create dynamic objects")]
    )

    bpy.types.Scene.create_multiple_yft = bpy.props.BoolProperty(
        name="Separate Objects", default=False)
    
    bpy.types.Scene.get_armature = bpy.props.PointerProperty(
        name="Armature", type=bpy.types.Object)
    
    bpy.types.Scene.bone_id_gen = bpy.props.IntProperty(
        name="Bone ID", default=0)
