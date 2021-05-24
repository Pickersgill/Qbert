from .queue import Queue
from .server import ServerGroup

class Kiosk:
    '''
    A Kiosk class. 

    Abstracts a model of a service in queue theory. Contains a group of servers (server_group) which
    can serve users/agents in a given time (service_time). The service provided is one of the 
    service_enums (colours) available.
        
    The Kiosk is situated in some environment which, it informs the registered environment when events
    occur. Abstractly, within the environment the Kiosk entrance is at some point (entrance) and when
    an agent collides with this point they are entered into the queue for this Kiosk. After the service
    time has passed the agent is removed from the queue and 'spat out' at the entrance.
    '''
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
        self.parent.unqueue_agent(agent, self)

    def get_service_time(self):
        return self.service_time

    def tick(self):
        self.server_group.tick()
        pass

    def __str__(self):
        r = f"KIOSK SERVING {str(self.service)} WITH "
        r += f"{len(self.queue)} AGENTS QUEUEING."
        return r
