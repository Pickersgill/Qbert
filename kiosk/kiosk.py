from .queue import Queue

class Kiosk:
    def __init__(self, servers, buffer_size, service_time, service):
        print(servers)
        print(service_time)
        print(service)
        self.queue = Queue()

    def add_to_queue(self, agent):
        self.queue.put(agent)
