import bpy
from bpy_extras.io_utils import ImportHelper
from .helper import open_ynv_file, build_mesh, get_mesh_data_from_ynv, create_navmesh_parent, set_nav_mesh_content_flags
from pathlib import Path

class Import_YNV(bpy.types.Operator, ImportHelper):
    bl_idname = "vicho.open_ynv"
    bl_label = "Import YNV(s)"
    bl_description = "Import YNV files"
    bl_options = {"REGISTER", "UNDO"}
    
    filename_ext = ".ynv"
    
    filter_glob: bpy.props.StringProperty(
        default="*.ynv",
        options={"HIDDEN"},
    )
    
    directory: bpy.props.StringProperty(
        subtype="DIR_PATH",
    )
    
    files: bpy.props.CollectionProperty(
        name="YNV files",
        type=bpy.types.OperatorFileListElement,
    )

    def execute(self, context):
        filepaths = [self.directory + f.name for f in self.files]
        for file in filepaths:
            ynv = open_ynv_file(file)
            ynv_name = Path(file).stem
            vertices_list, indices_list, flags_list = get_mesh_data_from_ynv(ynv)
            nav_mesh = build_mesh(vertices_list, indices_list, flags_list, "nav_mesh")
            new_parent = create_navmesh_parent(ynv_name)
            nav_mesh.parent = new_parent
            new_parent.navmesh_properties.UnkHash = str(ynv.Nav.VersionUnk2.Hash)
            new_parent.navmesh_properties.AreaID = ynv.Nav.AreaID
            set_nav_mesh_content_flags(ynv, new_parent)
        return {"FINISHED"}