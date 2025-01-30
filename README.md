# Django-Channels

### Adding Channels to Django Project
- At first install the `channels`.
    ```python
    pip install channels
    ```
- Include the `channels` inside the `settings.py`
    ```python
    INSTALLED_APPS = [
        'channels',
        ....
        ....
    ]
    ```
- Include `ASG_APPLICATION` inside the `settings.py`:
    ```python
    ASGI_APPLICATION = "projectname.asgi.application"
    ```
- Configure the `asgi.py`. At first remove this `application = get_asgi_application()` then include the bellow code.
    ```python
    from channels.routing import ProtocolTypeRouter
    
    application = ProtocolTypeRouter({
        "http": get_asgi_appication(),
        #Just HTTP for no. (We can other protocols later.)
    })
    ```


### **ProtocolTypeRouter:** 
- ProtocolTypeRouter lets you dispatch to one of a number of other ASGI applications based on the type value present in the scope.
- Protocols will define a fixed type value that their scope contains, so you can use this to distinguish between incoming connection types.
- ProtocolTypeRouter should be the top level of your ASGI application stack and the main entry in your routing file.
- It takes a single argument - a dictionary mapping type name to ASGI applications that server them:
    ```python
    ProtocolTypeRouter({
        "http":some_app,
        "websocket":some_other_app,
    })
    ```

## **Consumers:**
A consumer is the basic unit of Channels code. Consumers are like Django Views. Consumers do following things in particular:
- Structures your code as a series of functions to be called whenever an event happends, rather than making you write an event loop.
- Allow you to write synchoronus or async code and deals with handoffs and threading for you.

#### Creating Consumers:
A consumer is a subcalss of either SyncConsumer or AsyncConsumer.
- SyncConsumer
- AsyncConsumer

**SyncConsumer:** SyncConsumer will run your code synchronously in a threadpool.

**Step-by-step process of creating `SysncConsumer`:**
- First create a `consumers.py` file inside the application.
    ```python
    from channels.consumer import SyncConsumer
 
    class MySyncConsumer(SyncConsumer):

        def websocket_connect(self, event):
            print('WebSocket Connect...')
        
        def websocket_receive(self, event):
            print('Websocket Received..')
        
        def websocket_disconnect(self, event):
            print('Websocket Disconnect..')
    ```
    - `websocket_connect: `This handler is called when client initially opens a connection and is about to finish the WebSocket handshake.
    - `websocket_receive: ` This handler is called when data received from Client.
    - `websocket_disconnect: ` This handler is called when either connection to the client is lost, either from the client closing the connection, the server closing the connection, or loss of the socket.