from . import auto_load
from .vicho_dependencies import dependencies_manager as d, is_pythonnet_loaded, is_dotnet_installed

bl_info = {
    "name": "Vicho's Tools",
    "author": "MrVicho13",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "description": "Tools designed to help with GTA V modding",
    "category": "Vicho's Tools",
    "doc_url": "https://vichomodding.gitbook.io/main/blender-stuff/recommended-add-ons/modding/vichos-tools",
    "tracker_url": "https://github.com/Hancapo/VichoTools/issues",
}

auto_load.init()

def register():
    auto_load.register()
    if is_pythonnet_loaded() and is_dotnet_installed():
        d.load_dependencies()

def unregister():
    auto_load.unregister()

if __name__ == '__main__':
    register()
