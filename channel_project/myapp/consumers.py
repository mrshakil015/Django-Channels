# Topic - Consumer

from channels.consumer import SyncConsumer

class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self, event):
        print("Websocket Connected..")
    
    def websocket_receive(self, event):
        print("Message Received...")
    
    def websocket_disconnect(self, event):
        print("Websocket Disconnected")