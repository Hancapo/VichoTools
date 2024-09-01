import bpy


#exe, dll, rpf, asi, txt, asi, folder, dat

FILE_TYPES = [
    ('EXE', 'EXE', 'Executable file'),
    ('DLL', 'DLL', 'Dynamic Link Library file'),
    ('RPF', 'RPF', 'Rage Package File'),
    ('ASI', 'ASI', 'ASI file'),
    ('TXT', 'TXT', 'Text file'),
    ('FOLDER', 'FOLDER', 'Folder'),
    ('DAT', 'DAT', 'Data file')
]


class FileListProps(bpy.types.PropertyGroup):
    id: bpy.props.StringProperty(name="ID", default="")
    name: bpy.props.StringProperty(name="Name")
    file_type: bpy.props.EnumProperty(items=FILE_TYPES, name="File Type")
    path: bpy.props.StringProperty(name="Path")
    rpf_path: bpy.props.StringProperty(name="RPF Path")


def register():
    bpy.types.Scene.file_list = bpy.props.CollectionProperty(type=FileListProps)
    bpy.types.Scene.file_list_index = bpy.props.IntProperty(name="Active Index")
    bpy.types.Scene.file_list_current_path = bpy.props.StringProperty(name="Current Path")

def unregister():
    del bpy.types.Scene.file_list
    del bpy.types.Scene.file_list_index
    del bpy.types.Scene.file_list_current_path