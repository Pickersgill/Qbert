from .queue import Queue
from .server import ServerGroup

class Kiosk:
    def __init__(self, env, service, servers=1, service_time=1, entrance=(0, 0)):
        self.parent = env
        self.service = service
        self.service_time = service_time
        self.server_num = servers
        self.server_group = ServerGroup(self)
        self.queue = Queue()
        self.entrance = entrance

    def enqueue_agent(self, agent):
        self.queue.put(agent)

    def unqueue_agent(self, agent):
        self.parent.respawn_agent(agent, self.entrance)

    def get_service_time(self):
        return self.service_time

    def tick(self):
        self.server_group.tick()
        pass
