bl_info = {
    "name": "Vicho's Tools",
    "author": "MrVicho13",
    "version": (1, 0, 1),
    "blender": (4, 0, 0),
    "description": "A collection of tools for GTA V modding ranging from Textures, Animations, YMAP(S) and more.",
    "category": "Vicho's Tools",
    "doc_url": "https://vichomodding.gitbook.io/main/blender-stuff/recommended-add-ons/modding/vichos-tools",
    "tracker_url": "https://github.com/Hancapo/VichoTools/issues",
}

def reload_vicho_tools():
    import sys
    print("Reloading Vicho's Tools")
    
    
    from . import icons_load
    icons_load.unregister_icons()
    global auto_load
    del auto_load
    vicho_module_prefix = f"{__package__}."
    module_names = list(sys.modules.keys())
    for name in module_names:
        if name.startswith(vicho_module_prefix):
            del sys.modules[name]
            
if "auto_load" in locals():
    reload_vicho_tools()
    from .vicho_dependencies import dependencies_manager as d, is_pythonnet_loaded, is_dotnet_installed
    if is_pythonnet_loaded() and is_dotnet_installed():
        d.load_dependencies()

from . import auto_load
from . import icons_load
from .vicho_dependencies import dependencies_manager as d, is_pythonnet_loaded, is_dotnet_installed

auto_load.init()

def register():
    icons_load.init_icons()
    icons_load.load_icons()
    auto_load.register()
    if is_pythonnet_loaded() and is_dotnet_installed():
        d.load_dependencies()

def unregister():
    auto_load.unregister()
    icons_load.unregister_icons()