import hashlib

flags_updating = False
content_flags_updating = False

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


YMAP_MAP_DATA_TOGGLES = (
    ("DATA", "Data", "Data", "OUTLINER_DATA_LIGHTPROBE", 0),
    ("CONTENT_FLAGS", "Content Flags", "Content Flags", "OUTLINER_DATA_LIGHTPROBE", 1),
    ("FLAGS", "Flags", "Flags", "OUTLINER_OB_GROUP_INSTANCE", 2),
    ("STREAMING_EXTENTS", "Streaming Extents", "Streaming Extents", "GP_CAPS_ROUND", 3),
    ("ENTITIES_EXTENTS", "Entities Extents", "Entities Extents", "PHYSICS", 4),
)

map_data_content_flags_values = {
    "hd": 1,
    "lod": 2,
    "slod2+": 4,
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

def update_flags_bool_properties(self, context):
    global flags_updating
    if flags_updating:
        return
    flags_updating = True
    for key, value in map_data_flags_values.items():
        setattr(self, key, bool(self.total_flags & value))
    flags_updating = False
    
def update_flags(self, context):
    global flags_updating
    if flags_updating:
        return
    flags_updating = True
    self.total_flags = 0
    for key, value in map_data_flags_values.items():
        if getattr(self, key):
            self.total_flags |= value
    flags_updating = False
    
def update_content_flags_bool_properties(self, context):
    global content_flags_updating
    if content_flags_updating:
        return
    content_flags_updating = True
    for key, value in map_data_content_flags_values.items():
        setattr(self, key, bool(self.total_flags & value))
    content_flags_updating = False
    
def update_content_flags(self, context):
    global content_flags_updating
    if content_flags_updating:
        return
    content_flags_updating = True
    self.total_flags = 0
    for key, value in map_data_content_flags_values.items():
        if getattr(self, key):
            self.total_flags |= value
    content_flags_updating = False
    
def get_hash_from_bytes(data: bytes, algorithm:str = "sha256") -> str:
    """Returns the hash of the data"""
    hash_object = hashlib.new(algorithm)
    hash_object.update(data)
    return hash_object.hexdigest()