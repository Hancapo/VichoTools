import bpy

def register():
    bpy.types.Scene.is_vicho_server_running = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.is_vicho_gta_loaded = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.add_asset_to_scene = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.asset_ip = bpy.props.StringProperty(default="localhost")
    bpy.types.Scene.asset_port = bpy.props.IntProperty(default=5000, min=0, max=65535)

def unregister():
    del bpy.types.Scene.is_vicho_server_running
    del bpy.types.Scene.is_vicho_gta_loaded
    del bpy.types.Scene.add_asset_to_scene
    del bpy.types.Scene.asset_ip
    del bpy.types.Scene.asset_port