from enum import Enum

class EventEnum(Enum):
    COMPLETE_TASK = 1
    ASSIGN_TASK = 2
    JOIN_QUEUE = 3
    LEAVE_QUEUE = 4
    MOVE_TO = 5
    TURN_TO = 6
    FAIL_QUEUE = 7
    KIOSK_CREATED = 8
    AGENT_CREATED = 9

class CompleteTaskEvent:
    def __init__(self, agent, time, task):
        self.agent = agent
        self.time = time
        self.task = task
    
    def to_dict(self):
        json_dict = {
            "time" : self.time,
            "event" : EventEnum.COMPLETE_TASK.name,
            "agent" : id(self.agent),
            "task" : id(self.task) 
        }

        return json_dict

class AssignTaskEvent:
    def __init__(self, agent, time, task):
        self.agent = agent
        self.time = time
        self.task = task
    
    def to_dict(self):
        json_dict = {
            "time" : self.time,
            "event" : EventEnum.ASSIGN_TASK.name,
            "agent" : id(self.agent),
            "task" : id(self.task) 
        }

        return json_dict

class MoveEvent:
    def __init__(self, agent, time, pos):
        self.agent = agent
        self.time = time
        self.x = pos[0]
        self.y = pos[1]
    
    def to_dict(self):
        json_dict = {
            "time" : self.time,
            "event" : EventEnum.MOVE_TO.name,
            "agent" : id(self.agent),
            "x" : self.x,
            "y" : self.y 
        }

        return json_dict

class TurnEvent:
    def __init__(self, agent, time, direction):
        self.agent = agent
        self.time = time
        self.direction = direction
    
    def to_dict(self):
        json_dict = {
            "time" : self.time,
            "event" : EventEnum.TURN_TO.name,
            "agent" : id(self.agent),
            "direction" : self.direction
        }

        return json_dict

class FailQueueEvent:
    def __init__(self, agent, time):
        self.agent = agent
        self.time = time
    
    def to_dict(self):
        json_dict = {
            "time" : self.time,
            "event" : EventEnum.FAIL_QUEUE.name,
            "agent" : id(self.agent)
        }

        return json_dict
        

class JoinQueueEvent:
    def __init__(self, agent, time, kiosk):
        self.agent = agent
        self.time = time
        self.kiosk = kiosk
    
    def to_dict(self):
        json_dict = {
            "time" : self.time,
            "event" : EventEnum.JOIN_QUEUE.name,
            "agent" : id(self.agent),
            "kiosk" : id(self.kiosk)
        }

        return json_dict

class LeaveQueueEvent:
    def __init__(self, agent, time, kiosk):
        self.agent = agent
        self.time = time
        self.kiosk = kiosk
    
    def to_dict(self):
        json_dict = {
            "time" : self.time,
            "event" : EventEnum.LEAVE_QUEUE.name,
            "agent" : id(self.agent),
            "kiosk" : id(self.kiosk)
        }

        return json_dict

class CreateKioskEvent:
    def __init__(self, kiosk, time):
        self.kiosk_id = id(kiosk)
        self.time = time
        self.pos = kiosk.entrance
        self.service = kiosk.service
        self.servers = kiosk.server_num
        self.service_time = kiosk.service_time

    def to_dict(self):
        json_dict = {
            "time" : self.time,
            "event" : EventEnum.KIOSK_CREATED.name,
            "kiosk_id" : self.kiosk_id,
            "pos" : self.pos,
            "service" : self.service.name,
            "servers" : self.servers,
            "service_time" : self.service_time
        }

        return json_dict


class CreateAgentEvent:
    def __init__(self, agent, time):
        self.agent_id = id(agent)
        self.time = time
        self.pos = agent.position

    def to_dict(self):
        json_dict = {
            "time" : self.time,
            "event" : EventEnum.AGENT_CREATED.name,
            "agent_id" : self.agent_id,
            "pos" : self.pos
        }

        return json_dict


