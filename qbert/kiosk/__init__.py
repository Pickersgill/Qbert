try:
    from . import kiosk
    from . import queue
    from . import server
except:
    import kiosk
    import queue
    import server

Kiosk = kiosk.Kiosk
Queue = queue.Queue
Server = server.Server
ServerGroup = server.ServerGroup
