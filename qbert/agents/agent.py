from .actEnum import ActEnum, Act
from tasks import Task, TaskList

class DumbMind:
    def __init__(self):
        self.turned = False
        self.queued = False

    def tick(self, agent, env):
        if agent.queueing and not self.queued:
            self.queued = True

    def decide(self, agent, env):
        if self.queued:
            if self.turned:
                return Act(ActEnum.WALK, None)
            else:
                self.turned = True
                return Act(ActEnum.FACE, [180])
        elif env.time % 2 == 0:
            return Act(ActEnum.WALK, None)
        else:
            return Act(ActEnum.QUEUE, None) 


class Agent:
    def __init__(self, mind=None, name="DEFAULT"):
        self.mind = DumbMind() if mind is None else mind
        self.queueing = False
        self.position = (0, 0)
        self.facing = 0
        self.tasks = TaskList()
        self.name = name

    def tick(self, env):
        self.mind.tick(self, env)

    def decide(self, env):
        return self.mind.decide(self, env)

    def set_position(self, newpos):
        self.position = newpos

    def complete_task(self, service):
        if not self.tasks.empty():
            completed_task = self.tasks.get_highest_priority(service_filter=[service])
            if completed_task:
                completed_task.make_complete()
                return completed_task
        return None
    
    def _assign_task(self, task):
        self.tasks.append(task)
        
    def _assign_tasks(self, tasks):
        self.tasks += tasks

    def done(self):
        return self.tasks.all_complete()

    def __str__(self):
        r = f"AGENT {(self.name)} AT POSITION {self.position} " 
        r += f"FACING {self.facing} "
        r +=  f"WITH {len(self.tasks.get_remaining())} TASKS REMAINING."
        return r


        
