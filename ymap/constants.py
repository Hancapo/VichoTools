ymap_flags_updating = False
ymap_content_flags_updating = False
entity_flags_updating = False

YMAP_TYPE_TOGGLES = (
    ("MAPDATA", "Map Data", "Map Data", "OUTLINER_DATA_LIGHTPROBE", 0),
    ("ENTITIES", "Entities", "Entities", "OUTLINER_OB_GROUP_INSTANCE", 1),
    ("OCCLUDERS", "Occluders", "Occluders", "GP_CAPS_ROUND", 2),
    ("PHYSICSDICTIONARIES", "Physics Dictionaries", "Physics Dictionaries", "PHYSICS", 3),
    ("INSTANCEDDATA", "Instanced Data", "Instanced Data", "MOD_ARRAY", 4),
    ("TIMECYCLEMODIFIERS", "Timecycle Modifiers", "Timecycle Modifiers", "TIME", 5),
    ("CARGENERATORS", "Car Generators", "Car Generators", "AUTO", 6),
    ("LODLIGHTS", "Lod Lights", "Lod Lights", "LIGHTPROBE_PLANE", 7),
    ("DISTANTLIGHTS", "Distant Lights", "Distant Lights", "LIGHTPROBE_VOLUME", 8),
    ("BLOCK", "Block", "Block", "MESH_PLANE", 9),
)

ENTITY_TYPES = (
    ("ENTITY", "Entity", "Entity", "OUTLINER_DATA_LIGHTPROBE", 0),
    ("MLOINSTANCE", "MLO Instance", "MLO Instance", "HOME", 1),
)

YMAP_MAP_DATA_TOGGLES = (
    ("DATA", "Data", "Data", "OUTLINER_DATA_LIGHTPROBE", 0),
    ("CONTENT_FLAGS", "Content Flags", "Content Flags", "OUTLINER_DATA_LIGHTPROBE", 1),
    ("FLAGS", "Flags", "Flags", "OUTLINER_OB_GROUP_INSTANCE", 2),
    ("EXTENTS", "Extents", "Extents", "GP_CAPS_ROUND", 3)
)

ENTITY_TOGGLES = (
    ("DATA", "Data", "Data", "OUTLINER_DATA_LIGHTPROBE", 0),
    ("FLAGS", "Flags", "Flags", "OUTLINER_OB_GROUP_INSTANCE", 1),
    ("LOD", "LOD", "Lod", "GP_CAPS_ROUND", 2),
    ("AMBIENT_OCCLUSION", "Ambient Occlusion", "Ambient Occlusion", "PHYSICS", 3),
    ("MLO", "MLO", "MLO", "MOD_ARRAY", 4),
)

LOD_LEVELS = (
    ("LODTYPES_DEPTH_ORPHANHD", "Depth Orphan HD", "Depth Orphan HD", "OUTLINER_DATA_LIGHTPROBE", 0),
    ("LODTYPES_DEPTH_HD", "Depth HD", "Depth HD", "OUTLINER_OB_GROUP_INSTANCE", 1),
    ("LODTYPES_DEPTH_LOD", "Depth LOD", "Depth LOD", "GP_CAPS_ROUND", 2),
    ("LODTYPES_DEPTH_SLOD1", "Depth SLOD1", "Depth SLOD1", "PHYSICS", 3),
    ("LODTYPES_DEPTH_SLOD2", "Depth SLOD2", "Depth SLOD2", "MOD_ARRAY", 4),
    ("LODTYPES_DEPTH_SLOD3", "Depth SLOD3", "Depth SLOD3", "TIME", 5),
    ("LODTYPES_DEPTH_SLOD4", "Depth SLOD4", "Depth SLOD4", "AUTO", 6)
)

map_data_content_flags_values = {
    "hd": 1,
    "lod": 2,
    "slod2_plus": 4,
    "interior": 8,
    "slod": 16,
    "occlusion": 32,
    "physics": 64,
    "lod_lights": 128,
    "distant_lights": 256,
    "critical": 512,
    "grass": 1024
}

map_data_flags_values = {
    "script": 1,
    "lod": 2,
}

entity_flags_values = {
    "allow_full_rotation": 1,
    "stream_low_priority": 2,
    "disable_embedded_collision": 4,
    "lod_in_parent_map": 8,
    "lod_adopt_me": 16,
    "static_entity": 32,
    "interior_lod": 64,
    "lod_use_alt_fade": 32768,
    "underwater": 65536,
    "doesnt_touch_water": 131072,
    "doesnt_spawn_peds": 262144,
    "cast_static_shadows": 524288,
    "cast_dynamic_shadows": 1048576,
    "ignore_time_settings": 2097152,
    "dont_render_shadows": 4194304,
    "only_render_shadows": 8388608,
    "dont_render_reflections": 16777216,
    "only_render_reflections": 33554432,
    "dont_render_water_reflections": 67108864,
    "only_render_water_reflections": 134217728,
    "dont_render_mirror_reflections": 268435456,
    "only_render_mirror_reflections": 536870912,
}

COMPAT_SOLL_TYPES = [
    "sollumz_drawable",
    "sollumz_fragment",
]