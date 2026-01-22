from __future__ import annotations

VALID_NON_POLY_BOUND_TYPES: tuple[str, ...] = (
    "sollumz_bound_sphere",
    "sollumz_bound_box",
    "sollumz_bound_capsule",
    "sollumz_bound_disc",
    "sollumz_bound_geometry",
    "sollumz_bound_plane",
    "sollumz_bound_cylinder",
)

YMAP_ASSET_EXTS: tuple[str, ...] = ("ydr", "ydd", "yft", "ybn")

ENTITY_TYPES: tuple[tuple[str, str, str, str, int], ...] = (
    ("ENTITY", "Entity", "Entity", "OUTLINER_DATA_LIGHTPROBE", 0),
    ("MLOINSTANCE", "MLO Instance", "MLO Instance", "HOME", 1),
)

LOD_LEVELS: tuple[tuple[str, str, str, str, int], ...] = (
    ("LODTYPES_DEPTH_ORPHANHD", "Depth Orphan HD", "Depth Orphan HD", "EVENT_O", 0),
    ("LODTYPES_DEPTH_HD", "Depth HD", "Depth HD", "EVENT_H", 1),
    ("LODTYPES_DEPTH_LOD", "Depth LOD", "Depth LOD", "EVENT_L", 2),
    ("LODTYPES_DEPTH_SLOD1", "Depth SLOD1", "Depth SLOD1", "EVENT_ONEKEY", 3),
    ("LODTYPES_DEPTH_SLOD2", "Depth SLOD2", "Depth SLOD2", "EVENT_TWOKEY", 4),
    ("LODTYPES_DEPTH_SLOD3", "Depth SLOD3", "Depth SLOD3", "EVENT_THREEKEY", 5),
    ("LODTYPES_DEPTH_SLOD4", "Depth SLOD4", "Depth SLOD4", "EVENT_FOURKEY", 6),
)

PRIORITY_LEVELS: tuple[tuple[str, str, str, str, int], ...] = (
    ("PRI_OPTIONAL_HIGH", "Priority Optional High", "Priority Optional High", "OUTLINER_DATA_LIGHTPROBE", 0),
    ("PRI_OPTIONAL_MEDIUM", "Priority Optional Medium", "Priority Optional Medium", "OUTLINER_OB_GROUP_INSTANCE", 1),
    ("PRI_OPTIONAL_LOW", "Priority Optional Low", "Priority Optional Low", "OUTLINER_OB_GROUP_INSTANCE", 2),
    ("PRI_REQUIRED", "Priority Required", "Priority Required", "OUTLINER_OB_GROUP_INSTANCE", 3),
)

YMAP_MAP_DATA_TOGGLES: tuple[tuple[str, str, str, str, int], ...] = (
    ("DATA", "Data", "Data", "ALIGN_LEFT", 0),
    ("FLAGS", "Flags", "Flags", "PLAY", 2),
    ("EXTENTS", "Extents", "Extents", "AXIS_FRONT", 3),
)

ENTITY_TOGGLES: tuple[tuple[str, str, str, str, int], ...] = (
    ("DATA", "Data", "Data", "ALIGN_LEFT", 0),
    ("FLAGS", "Flags", "Flags", "PLAY", 1),
    ("LOD", "LOD", "Lod", "MOD_EXPLODE", 2),
    ("MISC", "Miscellaneous", "Miscellaneous", "OUTLINER_OB_EMPTY", 3),
    ("MLO", "MLO", "MLO", "HOME", 4),
)

MAP_DATA_CONTENT_FLAGS_VALUES: dict[str, int] = {
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
    "grass": 1024,
}

MAP_DATA_FLAGS_VALUES: dict[str, int] = {
    "script": 1,
    "lod": 2,
}

ENTITY_FLAGS_VALUES: dict[str, int] = {
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

SOLL_DRAWABLE: str = "sollumz_drawable"
SOLL_FRAGMENT: str = "sollumz_fragment"
SOLL_DRAWABLE_MODEL: str = "sollumz_drawable_model"
SOLL_DRAWABLE_DICTIONARY: str = "sollumz_drawable_dictionary"
SOLL_BOUND_COMPOSITE: str = "sollumz_bound_composite"

SOLLUM_TYPES: tuple[str, ...] = (
    SOLL_DRAWABLE,
    SOLL_FRAGMENT,
    SOLL_DRAWABLE_MODEL,
    SOLL_DRAWABLE_DICTIONARY,
    SOLL_BOUND_COMPOSITE,
)

YTD_SOLLUM_TYPES: tuple[str, ...] = (SOLL_DRAWABLE, SOLL_FRAGMENT, SOLL_DRAWABLE_DICTIONARY)
ANIM_SOLLUM_TYPES: tuple[str, ...] = (SOLL_DRAWABLE, SOLL_FRAGMENT)
YMAP_ENTITY_SOLLUM_TYPES: tuple[str, ...] = (SOLL_DRAWABLE, SOLL_FRAGMENT, SOLL_BOUND_COMPOSITE)

COMPAT_OBJECT_TYPES: tuple[str, ...] = ("EMPTY", "ARMATURE")

MAPENTITY_FLAGS: list[tuple[str, str, str]] = [
    ("1", "Allow Full Rotation", "Allow Full Rotation"),
    ("2", "Stream Low Priority", "Stream Low Priority"),
    ("4", "Disable Embedded Collision", "Disable Embedded Collision"),
    ("8", "LOD In Parent Map", "LOD In Parent Map"),
    ("16", "LOD Adopt Me", "LOD Adopt Me"),
    ("32", "Static Entity", "Static Entity"),
    ("64", "Interior LOD", "Interior LOD"),
    ("32768", "LOD Use Alt Fade", "LOD Use Alt Fade"),
    ("65536", "Underwater", "Underwater"),
    ("131072", "Doesn't Touch Water", "Doesn't Touch Water"),
    ("262144", "Doesn't Spawn Peds", "Doesn't Spawn Peds"),
    ("524288", "Cast Static Shadows", "Cast Static Shadows"),
    ("1048576", "Cast Dynamic Shadows", "Cast Dynamic Shadows"),
    ("2097152", "Ignore Time Settings", "Ignore Time Settings"),
    ("4194304", "Don't Render Shadows", "Don't Render Shadows"),
    ("8388608", "Only Render Shadows", "Only Render Shadows"),
    ("16777216", "Don't Render Reflections", "Don't Render Reflections"),
    ("33554432", "Only Render Reflections", "Only Render Reflections"),
    ("67108864", "Don't Render Water Reflections", "Don't Render Water Reflections"),
    ("134217728", "Only Render Water Reflections", "Only Render Water Reflections"),
    ("268435456", "Don't Render Mirror Reflections", "Don't Render Mirror Reflections"),
    ("536870912", "Only Render Mirror Reflections", "Only Render Mirror Reflections"),
]

GAME_VERSIONS: tuple[tuple[str, str, str], ...] = (
    ("Legacy", "Legacy", "Export asset for GTA V Legacy"),
    ("Enhanced", "Enhanced", "Export asset for GTA V Enhanced Edition"),
)

ARCH_TYPES: tuple[str, ...] = (
    "sollumz_archetype_base",
    "sollumz_archetype_time",
)

VALID_MAPDATA_ENTITY_FLAGS: int = sum(int(i[0]) for i in MAPENTITY_FLAGS)
