import bpy
from . import http_server
from http.server import HTTPServer
from .helper import load_gta_cache
from threading import Thread
from .helper import import_asset_from_pm, add_entity_to_scene
from ..vicho_dependencies import dependencies_manager as d

t1: Thread = None
server: HTTPServer = None

def import_loop():
    if not bpy.context.scene.is_vicho_server_running:
        return None
    if http_server.imported_asset != "":
        print("Received " + http_server.imported_asset)
        import_asset_from_pm(http_server.imported_asset, d.gamecache)
        if bpy.context.scene.add_asset_to_scene:
            add_entity_to_scene(http_server.imported_asset)
        http_server.imported_asset = ""
    return 0.1

def stop_server():
    global server, t1
    if server:
        try:
            server.shutdown()
            server.server_close()
            t1.join()
        except Exception as e:
            print("Error:", e)
        server = None

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
    
    
class VICHO_OT_load_game_files(bpy.types.Operator):
    """Load Game Files"""
    bl_idname = "assetimporter.load_game_files"
    bl_label = "Load GTA V Files"
    
    def execute(self, context):
        if load_gta_cache("C:/Program Files (x86)/Steam/steamapps/common/Grand Theft Auto V"):
            self.report({"INFO"}, "Game files successfully loaded")
            context.scene.is_vicho_gta_loaded = True
        else:
            self.report({"ERROR"}, "Couldn't load game files, try again.")
        return {'FINISHED'}