import bpy
from . import http_server
from http.server import HTTPServer
from threading import Thread
from ..vicho_dependencies import dependencies_manager as d
from .server import stop_server
from .helper import import_loop
from ..vicho_preferences import get_addon_preferences as prefs
from ..shared.helper import load_gta_cache
from bpy.app.handlers import persistent


class VICHO_OT_start_asset_server(bpy.types.Operator):
    """Starts the HTTP server to gather entities"""
    bl_idname = "assetimporter.start_server"
    bl_label = "Starts the HTTP server"
    
    def execute(self, context):
        scene = context.scene
        global t1, server
        is_server_loaded = scene.is_vicho_server_running
        if not is_server_loaded:
            server = HTTPServer((scene.asset_ip, scene.asset_port), http_server.AssetHandler)
            t1 = Thread(target=server.serve_forever, daemon=True)
            t1.start()
            bpy.app.timers.register(import_loop)
            scene.is_vicho_server_running = True
            self.report({'INFO'}, "Starting HTTP server...")
        else:
            Thread(target=stop_server, daemon=True).start()
            scene.is_vicho_server_running = False
            self.report({'INFO'}, "Stopping server...")
        return {'FINISHED'}

class VICHO_OT_load_gta_cache(bpy.types.Operator):
    """Load the GTA V game cache from the configured game folder."""
    bl_idname = "assetimporter.load_gta_cache"
    bl_label = "Load GTA V Game Cache"

    @classmethod
    def poll(cls, context):
        return prefs().gta5_dir is not None and d.gamecache is None
    
    def execute(self, context):
        if load_gta_cache(prefs().gta5_dir):
            self.report({"INFO"}, "Game files successfully loaded")
            context.scene.is_vicho_gta_loaded = True
        else:
            self.report({"ERROR"}, "Couldn't load game files, try again.")
        return {'FINISHED'}
    
class VICHO_OT_prompt_load_gta_cache(bpy.types.Operator):
    """Prompt the user to load the GTA V game cache."""
    bl_idname = "assetimporter.prompt_load_gta_cache"
    bl_label = "Load GTA V Game Cache"
    bl_options = {'INTERNAL'}

    
    def draw(self, context):
        layout = self.layout
        layout.label(
            text="Do you want to load the game cache?",
            icon='QUESTION'
        )

        if prefs().gta5_dir == "":
            layout.label(text="You need to set the GTA V, set it below, you can change it later if needed in the preferences.",icon='ERROR')
            layout.prop(prefs(), "gta5_dir", text="GTA V Directory")
            return

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def execute(self, context):
        bpy.ops.assetimporter.load_gta_cache()
        return {'FINISHED'}
    

def ask_to_load_cache():
    bpy.ops.assetimporter.prompt_load_gta_cache('INVOKE_DEFAULT')
    return None

@persistent
def on_blend_load(dummy):
    bpy.app.timers.register(ask_to_load_cache, first_interval=0.5)

def register():
    bpy.app.handlers.load_post.append(on_blend_load)

def unregister():
    bpy.app.handlers.load_post.remove(on_blend_load)
