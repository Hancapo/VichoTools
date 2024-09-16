from ..vicho_dependencies import dependencies_manager as d
import bpy

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
    

def open_ynv_file(file_path):
    """Open a YNV file and return the data as a dictionary."""
    ynv = d.YnvFile()
    ynv.Load(d.File.ReadAllBytes(file_path))
    return ynv

def create_navmesh_parent(name):
    """Create a parent object for the navmesh objects."""
    parent = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(parent)
    parent.vicho_type = "vicho_nav_mesh"
    return parent

def build_mesh(vertices_list, indices_list, name):
    """Build a single mesh from a list of lists of vertices and indices."""
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
    
    # Mensajes de depuración
    print(f"Combined vertices: {combined_vertices}")
    print(f"Combined indices: {combined_indices}")
    
    try:
        mesh.from_pydata(combined_vertices, [], combined_indices)
        mesh.update(calc_edges=True)
        mesh.validate(verbose=True)
    except Exception as e:
        print(f"Error al crear la malla: {e}")
        return None
    
    obj.vicho_type = "vicho_nav_mesh_geometry"
    return obj


def get_mesh_data_from_ynv(ynv):
    """Get lists of vertices and indices from a YNV file."""
    vertices_list = []
    indices_list = []
    
    for poly in ynv.Polys:
        vertices = [(point.X, point.Y, point.Z) for point in poly.Vertices]
        
        # poly.Indices es una lista de ushort
        indices = [int(i) for i in poly.Indices]
        
        vertices_list.append(vertices)
        indices_list.append(indices)
    
    return vertices_list, indices_list

def get_material(flags):
    """Generate a material based on the given flags."""
    mat = bpy.data.materials.new(name=str(flags))
    mat.use_nodes = True
    r = 0
    g = 0
    b = 0

    if flags & 1 > 0:
        r += 0.01  # avoid? loiter?
    if flags & 2 > 0:
        r += 0.01  # avoid?
    if flags & 4 > 0:
        g += 0.25  # ped/footpath
    if flags & 8 > 0:
        g += 0.02  # underground?
    if flags & 64 > 0:
        r += 0.25
    if flags & 128 > 0:
        b += 0.25

    if flags & 64 > 0:
        b += 0.1
    if flags & 512 > 0:
        g += 0.1
    if flags & 1024 > 0:
        b += 0.03
    if flags & 4096 > 0:
        g += 0.75
    if flags & 8192 > 0:
        b += 0.75
    if flags & 16384 > 0:
        r += 0.2
    if flags & 32768 > 0:
        b += 0.2
    if flags & 65536 > 0:
        g = 0.2

    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs[0].default_value = (r, g, b, 0.75)
    return mat