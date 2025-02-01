# Django-Channels

## Context
- [Django Channels Project Setup](#django-channels-project-setup)
- [ProtocolTypeRouter](#protocoltyperouter)
- [Consumers](#consumers)
    - [SyncConsumer](#syncconsumer)
    - [AsyncConsumer](#asyncconsumer)
- [Event](#event)
- [Routing](#routing)
- [Handle WebSocket from Frontend](#handle-websocket-from-frontend-javascript-in-django-channels)

### Django Channels Project Setup
- At first install the `channels` and `daphne`.
    ```python
    pip install channels
    pip install daphne
    ```
- Add `channels` and `daphne` to `INSTALLED_APPS` in `settings.py`. Add `daphne` at the top before `channels`:
    ```python
    INSTALLED_APPS = [
        'daphne',
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

⬆️[Go to Context](#context)
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
⬆️[Go to Context](#context)
## **Consumers:**
A consumer is the basic unit of Channels code. Consumers are like Django Views. Consumers do following things in particular:
- Structures your code as a series of functions to be called whenever an event happends, rather than making you write an event loop.
- Allow you to write synchoronus or async code and deals with handoffs and threading for you.


#### Creating Consumers:
A consumer is a subcalss of either SyncConsumer or AsyncConsumer.
- SyncConsumer
- AsyncConsumer

⬆️[Go to Context](#context)

### **SyncConsumer:**
SyncConsumer will run your code synchronously in a threadpool.

Step-by-step process of creating `SyncConsumer`:
- First create a `consumers.py` file inside the application.
    ```python
    from channels.consumer import SyncConsumer
 
    class MySyncConsumer(SyncConsumer):

        def websocket_connect(self, event):
            print('WebSocket Connect...')
            self.send({
                'type':'websocket.accept'
            })
        
        def websocket_receive(self, event):
            print('Websocket Received..')
            self.send({
                "type":"websocket.send",
                "text":"Message sent to client",
            })
        
        def websocket_disconnect(self, event):
            print('Websocket Disconnect..')
            raise StopConsumer()
    ```
    - `websocket_connect: `This handler is called when client initially opens a connection and is about to finish the WebSocket handshake.
    - `websocket_receive: ` This handler is called when data received from Client.
    - `websocket_disconnect: ` This handler is called when either connection to the client is lost, either from the client closing the connection, the server closing the connection, or loss of the socket.

        > Consumers are structured around a series of named methods correspoinding to the type value of the messages they are going to receive, with any ( . ) replaced by ( _ ) Example:- websocket.connect message is handled by websocket_connect

⬆️[Go to Context](#context)

### **AsyncConsumer:**
AsyncConsumer will expect you to write async-capable code.
- Step-by-step process of creating `AsyncConsumer`:
    ```python
    from channels.consumer import AsyncConsumer
    class MyAsyncConsumer(AsyncConsumer):
        async def websocket_connect(self, event):
            print("Websocket Connected..")
            await self.send({
                'type':'websocket.accept'
            })
        
        async def websocket_receive(self, event):
            print("Message Received...")
            await self.send({
                "type":"websocket.send",
                "text":"Message sent to client",
            })
        
        async def websocket_disconnect(self, event):
            print("Websocket Disconnected") 
            raise StopConsumer()
    ```

⬆️[Go to Context](#context)
## Events:
### Connect - recieve event:
- Sent to the application when client intially opens a connection and is about to finish the WebSocket handshake.
    ```python
    "type":"websocket.connect"
    ```
### Accept-send event:
- Sent by the application when it wishes to accept an incoming connection.
    ```python
    "type":"websocket.accept"
    "subprotocol":None
    "headers":[name,value] # Where name is header name and value u header value.
    ```

### Receive - receive envent:
- Sent to the applicatio when a data message is received from the client.
    ```python
    "type":"websocket.receive"
    "bytes":None #The message content, if it was binary mode, or None. Option: if missing, it is equivalent to None.
    "text":None #The message content, if it wase text mode, or None. Option; if missing, it is equivalent to None.
    ```
### Send - send event:
- Sent by the application to send a data message to the - client.
    ```python
    "type":"websocket.send"
    "bytes":None #The binary message content, if it was binary mode, or None. Optional; if missing, it is equivalent to None.
    ```
### Disconnect - receive event:
- Sent to the application when either connection to the cleint is lost, either from the client closing the connectionm the server closing the connection, or loss of the socket.
    ```python
    "type":"websocket.disconnect"
    "code": The websocket close code in int, as per the websocket spec.
    ```
### Close - send event:
- Sent by the application to tell the server to close the connection.
    ```python
    "type":"websocket.close"
    "code": The websocket close code in int, as per the websocket spec. Optional; if missing defaults to 1000.
    "reason":"no need" # A reason given for the closure, can be any string. Optional; if missing or None default is empty string.
    ```


⬆️[Go to Context](#context)
## Routing:
- Channels provides routing classes that allwo you to combine and stack your consumers (and any other valid ASGI application) to dispatch based on what the connection is.
- We call the as_asgi() classmethod when routing our consumers.
- This returns an ASGI wrapper application that will instantiate a new consumer instance for each connection or scope.
- This is similar to Django's as_view(), which plays the same role for pre-request instances of class-based views.

**How to configure routing:**
- Create `routing.py` file then write all websocket url patterns inside this file.
    ```python
    from django.urls import path
    from . import consumers

    websocket_urlpatterns = [
        path('ws/sc/',consumers.MySyncConsumer.as_asgi()),
        path('ws/ac/',consumers.MyAsyncConsumer.as_asgi()),
    ]
    ```
- Open `asgi.py` file and methioned your `routing.py` file.
    ```python
    from channels.routing import ProtocolTypeRouter,URLRouter
    from channels.auth import AuthMiddlewareStack
    import myapp.routing #import routing from the app

    application = ProtocolTypeRouter({
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack( 
            URLRouter(
                myapp.routing.websocket_urlpatterns
            )
        )
    })
    ```

⬆️[Go to Context](#context)

## Handle Websocket from Frontend JavaScript in Django Channels:
- The WebSocket object provides the API for creating and managing a WebSocket connection to a server, as well as for sending and receiving data on the connection.
- To construct a WebSocket, use the `WebSocket()` constructor.
    ```js
    var ws = new WebSocket('ws://127.0.1:8000/ws/sc/');
    ```

#### **WebSocket Properties:**
- `onopen - `The `WebSocket.onopen` property is an event handler that is called when the WebSocket connection's readyState changes to 1; this indicates that the connection is ready to send and receive data. It is called with an Event.
    ```js
    ws.onopen = function(event){
        console.log("WebSocket connection open",event);
    };
    ```
- `onmessage - `The `WebSocket.onmessage` property is an event handler that is called when a mssage is received from the server. It is called with a MessageEvent.
    ```js
    ws.onmessage = function(event){
        console.log("WebSocket message received from server",event);
    };
    ```
- `onerror - `The WebSocket interface's onerror event handler property is a function which gets called when an error occurs on the WebSocket.
    ```js
    ws.onerror = function(event){
        console.log("WebSocket Error Occurred",event);
    };
    ```
- `onclose - `The `WebSocket.onclose` property is an event handler that is called when the WebSocket connection's readyState changes to CLOSED. It is called with a CloseEvent.
    ```js
    ws.onclose = function(event){
        console.log("WebSocket Connection closed", event);
    };
    ```
#### **Events:**
- `open:` The open event is fired when a connection with a WebSocket is opened.
    ```js
    ws.addEventListener('open',(event)=>{
        console.log("WebSocket Connection Open");
    });
    ```
- `message:` The message event is fired when data is received through a WebSocket.
    ```js
    ws.addEventListener('message',(event)=>{
        console.log('WebSocket message received from server',event);
    });
    ```
- `error:` The error event is fired when a connection with a WebSocket has been closed due to an error:
    ```js
    ws.addEventListener('error',(event)=>{
        console.log('WebSocket Error Occurred',event);
    });
    ```
- `close:` The close event is fired when a connection with a WebSocket is closed.
    ```js
    ws.addEventListener('close',(event)=>{
        console.log('WebSocket connection closed',event);
    });
    ```

#### **Methods:**
- `close():` The `WebSocket.close()` method closes the websocket connection or connection attempt, if any. If the connection is already CLOSED, this method does nothing.
    ```js
    Syntax:- ws.close(code, reason)
    ```
    - `code-` A numeric value indicating the status code explaining why the connection is being closed. If this parameter is not specified, a default value of 1005 is assumed. See the list of status codes of CloseEvent for permitted values.
    - `reason-` A human-readable string explaining why the connection is closing. This string must be no  longer than 123 bytes of UTF-8 text (not characters)
    ```js
    ws.close()
    ```
- `send():` The `WebSocket.send()` method enqueues the specific data to be transmitted to the server over the websocket connection, increasing the value of buffered Amount by the number of butes need to contain the data. If the data can't be sent, the socket is closed automatically. The browser will throw an exception if you call send() when the connection is in the CONNECTING state.
If you call send() when the connection is in the CLOSING or CLOSED states, the browser will silenntly discard the data.

    ```js
    Syntax:- ws.send(data)
    ```
    ```js
    ws.send("Hello")
    ```
⬆️[Go to Context](#context)