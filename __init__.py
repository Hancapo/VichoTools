from . import auto_load

bl_info = {
    "name": "Vicho's Tools",
    "author": "MrVicho13",
    "version": (0, 7, 3),
    "blender": (4, 0, 0),
    "description": "Tools designed to help with GTA V modding",
    "category": "Vicho's Tools",
    "doc_url": "https://sollumz.gitbook.io/sollumz-wiki/",
    "tracker_url": "https://github.com/Hancapo/VichoTools/issues",
}

auto_load.init()

def register():
    auto_load.register()

def unregister():
    auto_load.unregister()

if __name__ == '__main__':
    register()
