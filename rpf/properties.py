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

#ymf, meta, ymt, ytd, ytyp, ymap, ydr, ybn, xml, yft
RPF_ENTRY_FILE_TYPES  = [
    ('YMF', 'YMF', 'Manifest file'),
    ('YTD', 'YTD', 'Texture Dictionary file'),
    ('YMAP', 'YMAP', 'Map Data file'),
    ('YDR', 'YDR', 'Drawable file'),
    ('YBN', 'YBN', 'Static Collision file'),
    ('XML', 'XML', 'XML file'),
    ('YFT', 'YFT', 'Fragment file'),
    ('YMT', 'YMT', 'Metadata (Binary) file'),
    ('YTYP', 'YTYP', 'Archetype Defition file'),
    ('DDS', 'DDS', 'DirectDraw Surface file'),
    ('META', 'META', 'Metadata (XML) file'),
    ('DAT', 'DAT', 'Cache file'),
    ('FXC', 'FXC', 'Compiled Shaders file'),
    ('SPS', 'SPS', 'Shader Preset file'),
    ('IDE', 'IDE', 'Item Definition file'),
    ('DAT', 'DAT', 'Data file'),
    ('YCD', 'YCD', 'Clip Dictionary file'),
    ('IPL', 'IPL', 'Item Placement file'),
    ('PSO', 'PSO', 'Metadata (PSO) file'),
    ('TXT', 'TXT', 'Text file'),
    ('BMP', 'BMP', 'Bitmap file'),
    ('FOLDER', 'FOLDER', 'Folder'),
    ('NONE', 'NONE', 'None')
]
    


class FileListProps(bpy.types.PropertyGroup):
    id: bpy.props.StringProperty(name="ID", default="")
    name: bpy.props.StringProperty(name="Name")
    file_type: bpy.props.EnumProperty(items=FILE_TYPES, name="File Type")
    path: bpy.props.StringProperty(name="Path")
    rpf_path: bpy.props.StringProperty(name="RPF Path")
    rpf_entry_type: bpy.props.EnumProperty(items=RPF_ENTRY_FILE_TYPES, name="RPF Entry Type")

def register():
    bpy.types.Scene.file_list = bpy.props.CollectionProperty(type=FileListProps)
    bpy.types.Scene.file_list_index = bpy.props.IntProperty(name="Active Index")
    bpy.types.Scene.file_list_current_path = bpy.props.StringProperty(name="Current Path")

def unregister():
    del bpy.types.Scene.file_list
    del bpy.types.Scene.file_list_index
    del bpy.types.Scene.file_list_current_path