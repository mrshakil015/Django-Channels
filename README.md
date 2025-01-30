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