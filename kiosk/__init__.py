try:
    from . import kiosk
    from . import queue
except:
    import kiosk
    import queue

Kiosk = kiosk.Kiosk
Queue = queue.Queue
