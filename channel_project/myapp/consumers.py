# Topic - Consumer

from channels.consumer import SyncConsumer,AsyncConsumer

class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self, event):
        print("Websocket Connected..")
    
    def websocket_receive(self, event):
        print("Message Received...")
    
    def websocket_disconnect(self, event):
        print("Websocket Disconnected")
        
class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Websocket Connected..")
    
    async def websocket_receive(self, event):
        print("Message Received...")
    
    async def websocket_disconnect(self, event):
        print("Websocket Disconnected")
        
