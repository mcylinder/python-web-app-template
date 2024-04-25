# Standard library imports
import os
import json
import datetime
import threading
import time

# Third party imports
import cherrypy
from jinja2 import Environment, FileSystemLoader
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import EchoWebSocket

# Configure CherryPy
cherrypy.config.update({'server.socket_port': 9001})
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()

class StringGenerator(object):
    # Class attributes
    handler = None
    env = Environment(loader=FileSystemLoader('templates'))

    def __init__(self):
        # Start a new thread that calls send_time every 3 seconds
        thread = threading.Thread(target=self.thread_function)
        thread.start()

    def thread_function(self):
        while True:
            self.send_time()
            time.sleep(3)

    @cherrypy.expose
    def index(self):
        # Render the page.html template with the current time
        template = self.env.get_template('page.html')
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return template.render(time_val_for_tmp=current_time)

    def send_time(self):
        # Send the current time to the WebSocket handler
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_string = json.dumps({"action": "update_time", "time": current_time})
        if self.handler:
            self.handler.send(data_string)

    @cherrypy.expose
    def ws(self):
        # Set the WebSocket handler
        self.handler = cherrypy.request.ws_handler

def run_server():
    # Configure CherryPy
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        },
        '/ws': {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': EchoWebSocket
        }
    }
    cherrypy.quickstart(StringGenerator(), '/', conf)

if __name__ == '__main__':
    run_server()