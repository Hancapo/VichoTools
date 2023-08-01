from mathutils import Matrix
import bmesh

def get_two_closest_vertices(v0, vertices):
    distances = [(vertex, (vertex - v0).length) for vertex in vertices]
    sorted_vertices = sorted(distances, key=lambda x: x[1])
    closest_vertices = [sorted_vertices[0][0], sorted_vertices[1][0]]
    return closest_vertices


def get_selected_vertex_coordinates(obj):
    if obj.mode != 'EDIT':
        raise ValueError("Object must be in edit mode")

    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    selected_verts = [v for v in bm.verts if v.select]
    selected_coords = [v.co.copy() for v in selected_verts]

    return selected_coords


def calculate_projection_matrix(selected_vertices):

    v0, v1, v2, v3 = selected_vertices

    a, b = get_two_closest_vertices(v0, [v1, v2, v3])

    T = v0
    U = (a - v0)
    V = (b - v0)

    tangent = (v3 - v0).normalized()

    m = Matrix.Identity(4)
    m[0][0:3] = T
    m[1][0:3] = V
    m[2][0:3] = U

    return m, tangent


def add_glass_window_to_list(glass_list, obj, self):
    if obj is not None and obj.type == 'MESH':
        selected_vertex_coordinates = get_selected_vertex_coordinates(obj)
        print(f"Selected vertex coordinates: {selected_vertex_coordinates}")
        projection_matrix, tangent = calculate_projection_matrix(
            selected_vertex_coordinates)
        if projection_matrix is None or tangent is None:
            self.report({'ERROR'}, f"Failed to calculate projection matrix")
            return False

        item = glass_list.add()
        item.name = f"GlassWindow{len(glass_list)}"
        item.projection.T = projection_matrix[0].xyz
        item.projection.U = projection_matrix[1].xyz
        item.projection.V = projection_matrix[2].xyz
        item.tangent = tangent
        return True
