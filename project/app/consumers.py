import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TerminalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Redirect stdout to send messages to the websocket
        sys.stdout = OutputRedirector(self.send_output_to_client)

    async def disconnect(self, close_code):
        # Reset stdout when websocket disconnects
        sys.stdout = sys.__stdout__

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

    async def send_output_to_client(self, message):
        await self.send(json.dumps({'message': message}))


#----------------------------------------------------------------
import sys
class OutputRedirector(object):
    def __init__(self, emit_function):
        self.emit_function = emit_function

    def write(self, message):
        self.emit_function(message)

    def flush(self):
        # This flush method is needed for Python 3 compatibility.
        # It will be called by the print function (which becomes print() in Python 3+).
        pass