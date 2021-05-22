from kiosk import Kiosk
from agents import ActEnum
from event import EventLogger

import math

WALK_DIST = 2
RUN_DIST = 2 * WALK_DIST
ENTRANCE_SIZE = 10


class Environment:


    def __init__(self, w=200, h=200):
        self.kiosks = list()
        self.agents = list()
        self.width = w
        self.height = h
        self.event_logger = EventLogger()
        self.time = 0

    def addKiosk(self, service=None, servers=1, service_time=1, position=0):
        ent = self.num_to_perimeter(position)
        newk = Kiosk(
              env=self,
              service=service, 
              servers=servers, 
              service_time=service_time, 
              entrance=ent
            )
    
        self.kiosks.append(newk)

    def addAgent(self, agent, position):
        self.agents.append(agent)
        agent.setPosition(position)
        print("SPAWNING NEW AGENT")

    def respawn_agent(self, agent, position):
        agent.setPosition(position)
        agent.queueing = False
        print(f"SPAWNING AGENT AT ({position[0]}, {position[1]})")

    def cycle(self):
        self.tick()
        self.decide()

    def tick(self):
        for agent in self.agents:
            agent.tick()
        for kiosk in self.kiosks:
            kiosk.tick()
        self.time += 1

    def decide(self):
        for agent in self.agents:
            if not agent.queueing:
                action = agent.decide(self)
                self.do(agent, action)

    def do(self, agent, action):
        t = action.act_type

        if t is ActEnum.WALK:
            self.doWalk(agent)
        elif t is ActEnum.RUN:
            self.doRun(agent)
        elif t is ActEnum.FACE:
            self.doFace(agent, *action.args)
        elif t is ActEnum.QUEUE:
            self.doQueue(agent)

    def doWalk(self, agent):
        print(f"AGENT: {str(agent)} IS WALKING")
        self._doMove(agent, WALK_DIST)
        
    def doRun(self, agent):
        # SAME AS WALK BUT WITH GREATER DISTANCE
        print(f"AGENT: {str(agent)} IS RUNNING")
        self._doMove(agent, RUN_DIST)

    def doFace(self, agent, direction):
        # SET AGENT TO FACE IN DIRECTION (DEGREES)
        print(f"AGENT: {str(agent)} IS CHANGING DIRECTION")
        agent.facing = direction

    def doQueue(self, agent):
        # JOIN QUEUE IF POSSIBLE
        near = self.get_nearest_kiosk(agent)
        if self.get_dist(agent.position, near.entrance) <= ENTRANCE_SIZE:
            self.enqueue(agent, near)
            self.event_logger.log(f"AGENT {str(agent)} JOINED QUEUE FOR {str(near)}")
           # TODO MAKE AN AGENT WALK TO A QUEUE AND JOIN
        else:
            self.event_logger.log(f"FAILED QUEUE ATTEMPT BY AGENT {str(agent)}")
    
    def _doMove(self, agent, dist):
        f = agent.facing
        cx = agent.position[0]
        cy = agent.position[1]
        
        nx = cx + round(dist * math.sin(math.radians(f)))
        ny = cy - round(dist * math.cos(math.radians(f)))

        if nx < 0:
            nx = 0
        elif nx > self.width:
            nx = self.width
        if ny < 0:
            ny = 0
        elif ny > self.height:
            ny = self.height

        agent.setPosition((nx, ny))
        self.emit(f"AGENT POSITION CHANGED TO {(nx, ny)}")

    def enqueue(self, agent, kiosk):
        agent.queueing = True
        kiosk.enqueue_agent(agent)

    def num_to_perimeter(self, num):
        w = self.width
        h = self.height
        num = num % (w + w + h + h)
        if num <= w:
            x = num
            y = 0
        elif num <= w + h:
            x = w
            y = num % w
        elif num <= w + w + h:
            x = w - num % w + h
            y = h
        elif num <= w + w + h + h:
            x = 0
            y = h - num % w + w + h
    
        return (x, y)

    def get_nearest_kiosk(self, agent):
        near_dist = -1
        near = None
        for kiosk in self.kiosks:
            c_dist = self.get_dist(agent.position, kiosk.entrance)
            if c_dist <= near_dist or near_dist == -1:
                near_dist = c_dist
                near = kiosk

        return near

    def get_dist(self, pos1, pos2):
        xdif = abs(pos1[0] - pos2[0])
        ydif = abs(pos1[1] - pos2[1])
        return math.sqrt(xdif * xdif + ydif * ydif)
        
    def emit(self, event):
        self.event_logger.log(event)
