from ..vicho_dependencies import dependencies_manager as d
import bpy
from math import pi

def set_nav_mesh_content_flags(ynv, obj):
    """Set the NavMeshContentFlags based on the given NavMeshFlags."""
    if ynv.Nav.ContentFlags.HasFlag(d.NavMeshFlags.Polygons):
        obj.navmesh_properties.ContentFlags.Polygons = True
    if ynv.Nav.ContentFlags.HasFlag(d.NavMeshFlags.Portals):
        obj.navmesh_properties.ContentFlags.Portals = True
    if ynv.Nav.ContentFlags.HasFlag(d.NavMeshFlags.Vehicle):
        obj.navmesh_properties.ContentFlags.Vehicle = True
    if ynv.Nav.ContentFlags.HasFlag(d.NavMeshFlags.Unknown8):
        obj.navmesh_properties.ContentFlags.Unknown8 = True
    if ynv.Nav.ContentFlags.HasFlag(d.NavMeshFlags.Unknown16):
        obj.navmesh_properties.ContentFlags.Unknown16 = True

def set_nav_poly_flags(obj):
    for mat in obj.material_slots:
        if mat:
            material = mat.material
            flags = int(material.name)
            if flags & 1:
                material.NavPolyFlagsA.SmallPoly = True
            if flags & 2:
                material.NavPolyFlagsA.LargePoly = True
            if flags & 4:
                material.NavPolyFlagsA.IsPavement = True
            if flags & 8:
                material.NavPolyFlagsA.IsUnderground = True
            if flags & 16:
                material.NavPolyFlagsA.Unused1 = True
            if flags & 32:
                material.NavPolyFlagsA.Unused2 = True
            if flags & 64:
                material.NavPolyFlagsA.IsTooSteepToWalk = True
            if flags & 128:
                material.NavPolyFlagsA.IsWater = True
                
            if flags & 256:
                material.NavPolyFlagsB.AudioProperties1 = True
            if flags & 512:
                material.NavPolyFlagsB.AudioProperties2 = True
            if flags & 1024:
                material.NavPolyFlagsB.AudioProperties3 = True
            if flags & 2048:
                material.NavPolyFlagsB.AudioProperties4 = True
            if flags & 4096:
                material.NavPolyFlagsB.Unused3 = True
            if flags & 8192:
                material.NavPolyFlagsB.NearCarNode = True
            if flags & 16384:
                material.NavPolyFlagsB.IsInterior = True
            if flags & 32768:
                material.NavPolyFlagsB.IsIsolated = True
                
            if flags & 65536:
                material.NavPolyFlagsC.ZeroAreaStitchPoly = True
            if flags & 131072:
                material.NavPolyFlagsC.CanSpawnPeds = True
            if flags & 262144:
                material.NavPolyFlagsC.IsRoad = True
            if flags & 524288:
                material.NavPolyFlagsC.LiesAlongEdgeOfMesh = True
            if flags & 1048576:
                material.NavPolyFlagsC.IsTraintrack = True
            if flags & 2097152:
                material.NavPolyFlagsC.IsShallowWater = True
            if flags & 4194304:
                material.NavPolyFlagsC.PedDensity1 = True
            if flags & 8388608:
                material.NavPolyFlagsC.PedDensity2 = True
            if flags & 16777216:
                material.NavPolyFlagsC.PedDensity3 = True
                
            if flags & 33554432:
                material.NavPolyFlagsD.CoverSouth = True
            if flags & 67108864:
                material.NavPolyFlagsD.CoverSouthEast = True
            if flags & 134217728:
                material.NavPolyFlagsD.CoverEast = True
            if flags & 268435456:
                material.NavPolyFlagsD.CoverNorthEast = True
            if flags & 536870912:
                material.NavPolyFlagsD.CoverNorth = True
            if flags & 1073741824:
                material.NavPolyFlagsD.CoverNorthWest = True
            if flags & 2147483648:
                material.NavPolyFlagsD.CoverWest = True
            if flags & 4294967296:
                material.NavPolyFlagsD.CoverSouthWest = True
def create_point_group(name="PointGroup"):
    point_grp = bpy.data.objects.new(name, None)
    point_grp.empty_display_size = 0
    bpy.context.collection.objects.link(point_grp)
    point_grp.vicho_type = "vicho_nav_point_group"
    return point_grp

def create_portal_group(name="PortalGroup"):
    portal_grp = bpy.data.objects.new(name, None)
    portal_grp.empty_display_size = 0
    bpy.context.collection.objects.link(portal_grp)
    return portal_grp       

def open_ynv_file(file_path):
    """Open a YNV file and return the data as a dictionary."""
    ynv = d.YnvFile()
    ynv.Load(d.File.ReadAllBytes(file_path))
    return ynv

def read_points(ynv):
    all_points = []
    if ynv.Points.Count > 0:
        for point in ynv.Points:
            print(f"Point: {point.Position.X}, {point.Position.Y}, {point.Position.Z}")
            point_obj = bpy.data.objects.new("NavPoint", None)
            point_obj.empty_display_size = 0.2
            point_obj.empty_display_type = "CUBE"
            point_obj.location = (point.Position.X, point.Position.Y, point.Position.Z)
            point_obj.rotation_euler.z = (point.Angle * 360 / 255) * (pi / 180)
            bpy.context.collection.objects.link(point_obj)
            point_obj.vicho_type = "vicho_nav_point"
            point_obj.navpoint_properties.Type = point.Type
            all_points.append(point_obj)
        return all_points
    else:
        return None

def create_navmesh_parent(name):
    """Create a parent object for the navmesh objects."""
    parent = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(parent)
    parent.vicho_type = "vicho_nav_mesh"
    return parent

def build_mesh(vertices_list, indices_list, flags_list, name):
    """Build a single mesh from a list of lists of vertices, indices, and flags."""
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    
    bpy.context.collection.objects.link(obj)
    
    combined_vertices = []
    combined_indices = []
    vertex_map = {}
    offset = 0
    
    for vertices, indices in zip(vertices_list, indices_list):
        for i, vertex in enumerate(vertices):
            if vertex not in vertex_map:
                vertex_map[vertex] = offset
                combined_vertices.append(vertex)
                offset += 1
            indices[i] = vertex_map[vertex]
        combined_indices.append(indices)
    
    try:
        mesh.from_pydata(combined_vertices, [], combined_indices)
        mesh.update(calc_edges=True)
        mesh.validate(verbose=True)
        
        # Assign materials based on flags
        material_map = {}
        for flags in set(flags_list):
            mat = get_material(flags)
            obj.data.materials.append(mat)
            material_map[flags] = obj.data.materials.find(mat.name)
        
        for poly, flags in zip(mesh.polygons, flags_list):
            poly.material_index = material_map[flags]
        
    except Exception as e:
        print(f"Error creating the mesh: {e}")
        return None
    
    obj.vicho_type = "vicho_nav_mesh_geometry"
    return obj


def get_mesh_data_from_ynv(ynv):
    """Get lists of vertices, indices, and flags from a YNV file."""
    vertices_list = []
    indices_list = []
    flags_list = []
    
    for poly in ynv.Polys:
        vertices = [(point.X, point.Y, point.Z) for point in poly.Vertices]
        
        # poly.Indices es una lista de ushort
        indices = [int(i) for i in poly.Indices]
        
        # Combine bitmask flags into a single integer for Flags1, Flags2, Flags3 and Flags4
        flags = poly.Flags1 | (poly.Flags2 << 8) | (poly.Flags3 << 17) | (poly.Flags4 << 25)
        
        vertices_list.append(vertices)
        indices_list.append(indices)
        flags_list.append(flags)
    
    return vertices_list, indices_list, flags_list

material_cache = {}

def get_material(flags):
    """Generate or retrieve a material based on the given flags."""
    # Check if material already exists in the cache
    if flags in material_cache:
        return material_cache[flags]
    
    mat_name = str(flags)
    mat = bpy.data.materials.get(mat_name)
    if mat is None:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        r, g, b = 0, 0, 0

        # Isolate flags1 from the bitmask
        flags1 = flags & 0xFF
        flags2 = (flags >> 8) & 0xFF
        flags3 = (flags >> 17) & 0xFF
        flags4 = (flags >> 25) & 0xFF
        
        # Set color based on flags1
        if flags1 & (1 << 0):
            r += 0.01  # avoid? loiter?
        if flags1 & (1 << 1):
            r += 0.01  # avoid?
        if flags1 & (1 << 2):
            g += 0.25  # ped/footpath
        if flags1 & (1 << 3):
            g += 0.02  # underground?
        if flags1 & (1 << 6):
            r += 0.25  # steep slope
        if flags1 & (1 << 7):
            b += 0.25  # water

        # Set color based on flags2
        if flags2 & (1 << 0):
            b += 0.1  # is interior?
        if flags2 & (1 << 1):
            g += 0.1  # is flat ground? ped-navigable?
        if flags2 & (1 << 2):
            b += 0.03  # is a road
        if flags2 & (1 << 3):
            g += 0.75  # is a train track
        if flags2 & (1 << 4):
            b += 0.75  # shallow water/moving water
        if flags2 & (1 << 5):
            r += 0.2  # footpaths/beach - peds walking?
        if flags2 & (1 << 6):
            b += 0.2  # footpaths - special?
        if flags2 & (1 << 7):
            g = 0.2  # footpaths - mall areas? eg mall, vinewood blvd



        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs[0].default_value = (r, g, b, 0.75)
    
    # Store material in cache for future use
    material_cache[flags] = mat
    return mat