class ServerNotFreeError(Exception):
    def __init__(self, message="Server is currently serving an agent."):
        super().__init__(message)

class Server:
    '''
    Server class must:
        
        - contain an agent currently being served
        - release the agent when service is complete
        - notify servergroup that agent is served

    '''
    def __init__(self, server_group):
        self.free = True
        self.serving = None
        self.serving_time = 0
        self.parent = server_group

    def serve(self, agent):
        if self.free:
            self.free = False
            self.serving = agent
            self.serving_time = 0
        else:
            raise ServerNotFreeError

    def unserve(self):
        self.free = True
        self.parent.unserve(self.serving)
        self.serving = None

    def tick(self):
        self.serving_time += 1
        if self.serving_time >= self.parent.serve_time and self.serving:
            self.unserve()
        

class ServerGroup:
    def __init__(self, parent_kiosk):
        self.parent = parent_kiosk
        self.serve_time = parent_kiosk.service_time
        self.servers = list(Server(self) for i in range(self.parent.server_num))

    def unserve(self, agent):
        self.parent.unqueue_agent(agent)

    def serve_agents(self):
        for server in self.servers:
            if server.free and not self.parent.queue.empty():
                server.serve(self.parent.queue.pop())

    def tick(self):
        self.serve_agents()
        for server in self.servers:
            server.tick()


