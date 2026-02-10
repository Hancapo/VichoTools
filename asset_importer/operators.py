import bpy
from . import http_server
from http.server import HTTPServer
from threading import Thread
from .server import stop_server
from .helper import import_loop


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
    
    
