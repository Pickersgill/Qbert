from kiosk import Kiosk
from agents import ActEnum
from event import EventLogger, CompleteTaskEvent, AssignTaskEvent, MoveEvent, TurnEvent, JoinQueueEvent, LeaveQueueEvent, FailQueueEvent, CreateKioskEvent, CreateAgentEvent
from . import env_utils

import math

WALK_DIST = 5
RUN_DIST = 2 * WALK_DIST
ENTRANCE_SIZE = 10


class Environment:

    def __init__(self, w=200, h=200, time_limit=1000):
        self.kiosks = list()
        self.agents = list()
        self.width = w
        self.height = h
        self.event_logger = EventLogger(w, h, time_limit)
        self.time_limit = time_limit
        self.time = 0

    def add_kiosk(self, service=None, servers=1, service_time=1, position=None):
        ent = env_utils.num_to_perimeter(self, position)
        newk = Kiosk(
              env=self,
              service=service, 
              servers=servers, 
              service_time=service_time, 
              entrance=ent
            )
    
        self.kiosks.append(newk)
        self.emit(CreateKioskEvent(newk, self.time))

    def add_agent(self, agent, position):
        self.agents.append(agent)
        agent.set_position(position)
        self.emit(CreateAgentEvent(agent, self.time))

    def unqueue_agent(self, agent, kiosk):
        agent.set_position(kiosk.entrance)
        completed_task = agent.complete_task(kiosk.service)
        agent.queueing = False
        self.emit(LeaveQueueEvent(agent, self.time, kiosk))
        if completed_task:
            self.emit(CompleteTaskEvent(agent, self.time, completed_task))

    def assign_task(self, agent, task):
        agent._assign_task(task)
        self.emit(AssignTaskEvent(agent, self.time, task))
    
    def assign_tasks(self, agent, tasks):
        for t in tasks:
            self.assign_task(agent, t)

    def cycle(self):
        self.tick()
        self.decide()

    def tick(self):
        for agent in self.agents:
            agent.tick(self)
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
            self.do_walk(agent)
        elif t is ActEnum.RUN:
            self.do_run(agent)
        elif t is ActEnum.FACE:
            self.do_face(agent, *action.args)
        elif t is ActEnum.QUEUE:
            self.do_queue(agent)
        elif t is ActEnum.IDLE:
            self.do_idle(agent, *action.args)

    def do_walk(self, agent):
        self._do_move(agent, WALK_DIST)
        
    def do_run(self, agent):
        # SAME AS WALK BUT WITH GREATER DISTANCE
        self._do_move(agent, RUN_DIST)

    def do_face(self, agent, direction):
        # SET AGENT TO FACE IN DIRECTION (DEGREES)
        agent.facing = direction
        self.emit(TurnEvent(agent, self.time, direction))

    def do_queue(self, agent):
        # JOIN QUEUE IF POSSIBLE
        near = env_utils.get_nearest_kiosk(agent, self)
        if env_utils.get_dist(agent.position, near.entrance) <= ENTRANCE_SIZE:
            self.enqueue(agent, near)
            self.emit(JoinQueueEvent(agent, self.time, near))
        else:
            self.emit(FailQueueEvent(agent, self.time))
    
    def do_idle(self, agent, message=""):
        pass

    def _do_move(self, agent, dist):
        f = agent.facing
        cx = agent.position[0]
        cy = agent.position[1]
        
        nx = cx + (dist * math.sin(math.radians(f)))
        ny = cy - (dist * math.cos(math.radians(f)))

        if nx < 0:
            nx = 0
        elif nx > self.width:
            nx = self.width
        if ny < 0:
            ny = 0
        elif ny > self.height:
            ny = self.height

        agent.set_position((nx, ny))
        self.emit(MoveEvent(agent, self.time, (nx, ny)))

    def enqueue(self, agent, kiosk):
        agent.queueing = True
        kiosk.enqueue_agent(agent)

    def emit(self, event):
        self.event_logger.log(event)

    def should_terminate(self):
        if self.time_limit > 0 and self.time >= self.time_limit:
            print("TERMINATING DUE TO TIME LIMIT: FAILURE")
            return True

        term = True
        for agent in self.agents:
            if not agent.done():
                return False
        
        print("##############ALL AGENTS DONE#############")
        print("SUCCESS AT TIME: ", self.time)

        return term


