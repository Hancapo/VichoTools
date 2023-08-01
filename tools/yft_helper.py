import bpy


def get_sollumz_bound_names():
    return ["sollumz_bound_box",
            "sollumz_bound_sphere",
            "sollumz_bound_capsule",
            "sollumz_bound_cylinder",
            "sollumz_bound_disc",
            "sollumz_bound_poly_triangle"]


def create_child_by_cols(sel_cols, scene, material_density):
    for i, col in enumerate(sel_cols):
        if col.sollum_type in get_sollumz_bound_names():
            obj_loc = col.location
            child_name = col.name.split("_col")[0] + "_child" + str(i)
            FragChild = bpy.data.objects.new(child_name, None)
            FragChild.empty_display_type = 'PLAIN_AXES'
            FragChild.location = obj_loc
            FragChild.sollum_type = 'sollumz_fragchild'
            FragChild.parent = col.parent
            FragChild.child_properties.pristine_mass = calculate_mass(col)
            FragChild.child_properties.damaged_mass = calculate_mass(col)# * 0.2
            scene.collection.objects.link(FragChild)


def calculate_mass(obj, material_density=1000):
    dimensions = obj.dimensions
    volume = dimensions[0] * dimensions[1] * dimensions[2]
    return volume * material_density


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


def assign_bone_flags_to_selection(armature, scene):
    selected_bones = [bone for bone in armature.data.edit_bones if bone.select]

    for bone in selected_bones:
        bone_props_name = "bone_properties"

        if bone_props_name not in bone.keys():
            bone[bone_props_name] = {}
            bone[bone_props_name]["flags"] = []

        new_flags = []

        for prop_name in ["TransX", "TransY", "TransZ", "RotX", "RotY", "RotZ", "ScaleX", "ScaleY", "ScaleZ"]:
            prop_value = getattr(scene, f'fragbonetag_{prop_name.lower()}')
            if prop_value:
                new_flags.append({"name": prop_name})

        # Reemplazar los flags antiguos con los nuevos
        bone[bone_props_name]["flags"] = new_flags