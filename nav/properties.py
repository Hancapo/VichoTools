import bpy

#description, icon, identifier

vicho_type = [
    ("vicho_none", "None", "None"),
    ("vicho_nav_mesh", "Nav Mesh", "Nav Mesh"),
    ("vicho_nav_mesh_geometry", "Nav Mesh Geometry", "Nav Mesh Geometry"),
    ("vicho_nav_poly", "Nav Poly", "Nav Poly"),
    ("vicho_nav_point_group", "Nav Point Group", "Nav Point Group"),
    ("vicho_nav_point", "Nav Point", "Nav Point"),
    ("vicho_nav_portal_group", "Nav Portal Group", "Nav Portal Group"),
    ("vicho_nav_portal", "Nav Portal", "Nav Portal"),]


class NavMeshContentFlags(bpy.types.PropertyGroup):
    Polygons: bpy.props.BoolProperty(name="Polygons", default=False)
    Portals: bpy.props.BoolProperty(name="Portals", default=False)
    Vehicle: bpy.props.BoolProperty(name="Vehicles", default=False)
    Unknown8: bpy.props.BoolProperty(name="Unknown 8", default=False)
    Unknown16: bpy.props.BoolProperty(name="Unknown 10", default=False)

class NavPolyFlagsA(bpy.types.PropertyGroup):
    SmallPoly: bpy.props.BoolProperty(name="Small Poly", default=False)
    LargePoly: bpy.props.BoolProperty(name="Large Poly", default=False)
    IsPavement: bpy.props.BoolProperty(name="Is Pavement", default=False)
    IsUnderground: bpy.props.BoolProperty(name="Is Underground", default=False)
    Unused1: bpy.props.BoolProperty(name="Unused 1", default=False)
    Unused2: bpy.props.BoolProperty(name="Unused 2", default=False)
    IsTooSteepToWalk: bpy.props.BoolProperty(name="Is Too Steep To Walk", default=False)
    IsWater: bpy.props.BoolProperty(name="Is Water", default=False)
    
    
class NavPolyFlagsB(bpy.types.PropertyGroup):
    AudioProperties1: bpy.props.BoolProperty(name="Audio Properties 1", default=False)
    AudioProperties2: bpy.props.BoolProperty(name="Audio Properties 2", default=False)
    AudioProperties3: bpy.props.BoolProperty(name="Audio Properties 3", default=False)
    AudioProperties4: bpy.props.BoolProperty(name="Audio Properties 4", default=False)
    Unused3: bpy.props.BoolProperty(name="Unused 3", default=False)
    NearCarNode: bpy.props.BoolProperty(name="Near Car Node", default=False)
    IsInterior: bpy.props.BoolProperty(name="Is Interior", default=False)
    IsIsolated: bpy.props.BoolProperty(name="Is Isolated", default=False)
    
class NavPolyFlagsC(bpy.types.PropertyGroup):
    ZeroAreaStitchPoly: bpy.props.BoolProperty(name="Zero Area Stitch Poly", default=False)
    CanSpawnPeds: bpy.props.BoolProperty(name="Can Spawn Peds", default=False)
    IsRoad: bpy.props.BoolProperty(name="Is Road", default=False)
    LiesAlongEdgeOfMesh: bpy.props.BoolProperty(name="Lies Along Edge Of Mesh", default=False)
    IsTraintrack: bpy.props.BoolProperty(name="Is Traintrack", default=False)
    IsShallowWater: bpy.props.BoolProperty(name="Is Shallow Water", default=False)
    PedDensity1: bpy.props.BoolProperty(name="Ped Density 1", default=False)
    PedDensity2: bpy.props.BoolProperty(name="Ped Density 2", default=False)
    PedDensity3: bpy.props.BoolProperty(name="Ped Density 3", default=False)
    
class NavPolyFlagsD(bpy.types.PropertyGroup):
    CoverSouth: bpy.props.BoolProperty(name="Cover South", default=False)
    CoverSouthEast: bpy.props.BoolProperty(name="Cover South East", default=False)
    CoverEast: bpy.props.BoolProperty(name="Cover East", default=False)
    CoverNorthEast: bpy.props.BoolProperty(name="Cover North East", default=False)
    CoverNorth: bpy.props.BoolProperty(name="Cover North", default=False)
    CoverNorthWest: bpy.props.BoolProperty(name="Cover Norh West", default=False)
    CoverWest: bpy.props.BoolProperty(name="Cover West", default=False)
    CoverSouthWest: bpy.props.BoolProperty(name="Cover South West", default=False)

class AreaIdProps(bpy.types.PropertyGroup):
    X: bpy.props.IntProperty(name="X", default=0, min=0, max=99)
    Y: bpy.props.IntProperty(name="Y", default=0, min=0, max=99)

class NavMeshProperties(bpy.types.PropertyGroup):
    AreaID: bpy.props.IntProperty(name="Area ID", default=0, min=0, max=9999)
    UnkHash: bpy.props.StringProperty(name="Unk Hash", default="0")
    ContentFlags: bpy.props.PointerProperty(type=NavMeshContentFlags)

class NavPointProperties(bpy.types.PropertyGroup):
    Type: bpy.props.IntProperty(name="Type", default=0, min=0, max=255)
    
class NavPortalFromProperties(bpy.types.PropertyGroup):
    FromAreaID: bpy.props.IntProperty(name="From Area ID", default=0, min=0, max=9999)
    FromPolyID1: bpy.props.IntProperty(name="From Poly ID", default=0, min=0, max=9999)
    FromPolyID2: bpy.props.IntProperty(name="From Poly ID", default=0, min=0, max=9999)
    Unk1: bpy.props.IntProperty(name="Unk 1", default=0, min=0, max=9999)
    
class NavPortalToProperties(bpy.types.PropertyGroup):
    ToAreaID: bpy.props.IntProperty(name="To Area ID", default=0, min=0, max=9999)
    ToPolyID1: bpy.props.IntProperty(name="To Poly ID", default=0, min=0, max=9999)
    ToPolyID2: bpy.props.IntProperty(name="To Poly ID", default=0, min=0, max=9999)
    Unk2: bpy.props.IntProperty(name="Unk 2", default=0, min=0, max=9999)
    
class NavPortalProperties(bpy.types.PropertyGroup):
    From: bpy.props.PointerProperty(type=NavPortalFromProperties)
    To: bpy.props.PointerProperty(type=NavPortalToProperties)

def register():
    bpy.types.Object.vicho_type = bpy.props.EnumProperty(
        items=vicho_type,
        name="Vicho Type",
        default="vicho_none",
        description="Type of object",
    )
    bpy.types.Object.navmesh_properties = bpy.props.PointerProperty(type=NavMeshProperties)
    bpy.types.Object.navpoint_properties = bpy.props.PointerProperty(type=NavPointProperties)
    bpy.types.Object.navportal_properties = bpy.props.PointerProperty(type=NavPortalProperties)
    
def unregister():
    del bpy.types.Object.vicho_type
    del bpy.types.Object.navmesh_properties
    del bpy.types.Object.navpoint_properties
    del bpy.types.Object.navportal_properties