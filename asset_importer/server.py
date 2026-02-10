from threading import Thread
from http.server import HTTPServer

t1: Thread = None
server: HTTPServer = None

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