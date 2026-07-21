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

from . import auto_load  # noqa: E402
from . import icons_load # noqa: E402

#from .ymap import key_maps # noqa: E402

auto_load.init()

def register():
    icons_load.init_icons()
    icons_load.load_icons()
    auto_load.register()

def unregister():
    auto_load.unregister()
    icons_load.unregister_icons()