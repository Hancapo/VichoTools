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
            FragChild.child_properties.damaged_mass = calculate_mass(
                col)  # * 0.2
            scene.collection.objects.link(FragChild)


def calculate_mass(obj, material_density=1000):
    dimensions = obj.dimensions
    volume = dimensions[0] * dimensions[1] * dimensions[2]
    return volume * material_density


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


def apply_def_props_to_fragment(frag):
    frag.fragment_properties.unk_b0 = 0.0
    frag.fragment_properties.unk_b8 = 0.0
    frag.fragment_properties.unk_bc = 0.0
    frag.fragment_properties.unk_c0 = 0.0
    frag.fragment_properties.unk_c4 = 1.0
    frag.fragment_properties.unk_cc = 0.0
    frag.fragment_properties.gravity_factor = 1.0
    frag.fragment_properties.bouyancy_factor = 1.0


def apply_def_props_to_fragment_lod(frag_lod):
    frag_lod.lod_properties.type = 1
    frag_lod.lod_properties.unk_14 = 0
    frag_lod.lod_properties.unk_18 = 0
    frag_lod.lod_properties.unk_1c = 0
    frag_lod.lod_properties.position_offset = (0.0, 0.0, 0.0)
    frag_lod.lod_properties.unknown_40 = (0.0, 0.0, 0.0)
    frag_lod.lod_properties.unknown_50 = (0.0, 0.0, 0.0)
    frag_lod.lod_properties.damping_linear_c = (0.02, 0.02, 0.02)
    frag_lod.lod_properties.damping_linear_v = (0.02, 0.02, 0.02)
    frag_lod.lod_properties.damping_linear_c2 = (0.01, 0.01, 0.01)
    frag_lod.lod_properties.damping_linear_v2 = (0.01, 0.01, 0.01)
    frag_lod.lod_properties.damping_angular_c = (0.02, 0.02, 0.02)
    frag_lod.lod_properties.damping_angular_v = (0.02, 0.02, 0.02)
    frag_lod.lod_properties.damping_angular_v2 = (0.01, 0.01, 0.01)

    # Archetype properties
    frag_lod.lod_properties.archetype_name = frag_lod.parent.name
    frag_lod.lod_properties.archetype_mass = 600
    frag_lod.lod_properties.archetype_unknown_48 = 1
    frag_lod.lod_properties.archetype_unknown_4c = 150
    frag_lod.lod_properties.archetype_unknown_50 = 6.28
    frag_lod.lod_properties.archetype_unknown_54 = 1
    frag_lod.lod_properties.archetype_inertia_tensor = (1.0, 1.0, 1.0)


def create_sollumz_armature(objs, add_flags=True, create_multiples=False, initial_bone_id=0):
    if not create_multiples:
        name = 'new_yft'
        bpy.ops.object.add(type='ARMATURE', enter_editmode=True)
        armature_obj = bpy.context.active_object
        armature_obj.name = f"{name}_skel"
        armature_data = armature_obj.data
        armature_data.name = f"{name}.skel"
        bone = armature_data.edit_bones.new(name)
        armature_obj.sollum_type = 'sollumz_drawable'
        bone.head = (0, 0, 0)
        bone.tail = (0, 0.05, 0)
        bone.head_radius = 0.1
        bone.tail_radius = 0.05
        bone.roll = 0
        bone.length = 0.05
        bone.envelope_distance = 0.25
        bone.use_connect = False
        bone_props_name = "bone_properties"
        if bone_props_name not in bone.keys():
            bone[bone_props_name] = {}
            bone[bone_props_name]["flags"] = []
        if add_flags:
            new_flags = [
                {'name': 'RotX'},
                {'name': 'RotY'},
                {'name': 'RotZ'},
                {'name': 'TransX'},
                {'name': 'TransY'},
                {'name': 'TransZ'}
            ]
            bone[bone_props_name]["flags"] = new_flags
        bpy.ops.object.mode_set(mode='OBJECT')
        print(objs)
        create_bones_for_drawables(objs, bone, initial_bone_id)
        return armature_obj
    else:
        return False


def create_bones_for_drawables(objs, mainbone, boneid=24000):
    bone_name = mainbone.name
    armature = bpy.context.active_object
    bpy.ops.object.mode_set(mode='EDIT')
    mainbone = armature.data.edit_bones[bone_name]
    for obj in objs:
        if obj.sollum_type == 'sollumz_drawable_model':
            obj.parent = armature
            bone = armature.data.edit_bones.new(obj.name)
            bone.head = (0, 0, 0)
            bone.tail = (0, 0.05, 0)
            bone.head_radius = 0.1
            bone.tail_radius = 0.05
            bone.roll = 0
            bone.length = 0.05
            bone.envelope_distance = 0.25
            bone.use_connect = False
            bone.matrix = obj.matrix_world
            bone.parent = mainbone
            obj.delta_location.y = -0.05
            obj.parent_type = 'BONE'
            obj.parent_bone = bone.name
            obj.location = (0, 0, 0)
            boneid += 1
            bone_props_name = "bone_properties"
            if bone_props_name not in bone.keys():
                bone[bone_props_name] = {}
                bone[bone_props_name]["tag"] = boneid
    bpy.ops.object.mode_set(mode='OBJECT')
    


def create_sollumz_drawable(obj):
    obj.name = f"{obj.name}_geom"
    empty_name = obj.name[:-5]
    bpy.ops.object.add(type='EMPTY', location=obj.location)
    empty_obj = bpy.context.active_object
    empty_obj.name = empty_name
    obj_matrix = obj.matrix_world.copy()
    obj.location = (0, 0, 0)
    obj.rotation_euler = (0, 0, 0)
    obj.scale = (1, 1, 1)
    empty_obj.matrix_world = obj_matrix
    obj.parent = empty_obj
    obj.sollum_type = 'sollumz_drawable_geometry'
    empty_obj.sollum_type = 'sollumz_drawable_model'
    return empty_obj
