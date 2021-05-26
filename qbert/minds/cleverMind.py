from agents import Agent, DumbMind, ActEnum, Act
from environment import Env, env_utils
from tasks import Task, TaskList

class CleverMind:
    def __init__(self):
        self.heading = False
        pass

    def tick(self, agent, env):
        pass
    
    def decide(self, agent, env):

        task = agent.tasks.get_highest_priority()
        if task:
            dest = env_utils.get_nearest_kiosk(agent, env, [task.service])
        else:
            dest = None
        
        if not self.heading:
            angle = env_utils.get_angle_from(agent.position, dest.entrance)
            self.heading = True
            return Act(ActEnum.FACE, [angle])

        if not agent.done() and env_utils.can_join(agent, env, dest):
            return Act(ActEnum.QUEUE, [dest])

        if not agent.done():
            return Act(ActEnum.WALK, None)

        return Act(ActEnum.IDLE)

