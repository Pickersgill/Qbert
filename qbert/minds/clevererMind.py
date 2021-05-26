from agents import Agent, DumbMind, ActEnum, Act
from environment import Env, env_utils
from tasks import Task, TaskList

class ClevererMind:
    def __init__(self):
        self.headingHome = False
        self.home = False
        pass

    def tick(self, agent, env):
        pass
    
    def decide(self, agent, env):

        task = agent.tasks.get_highest_priority()
        if task:
            dest = env_utils.get_nearest_kiosk(agent, env, [task.service])
            correctAngle = env_utils.get_angle_from(agent.position, dest.entrance)

            if agent.facing != correctAngle:
                return Act(ActEnum.FACE, [correctAngle])

            if not agent.done() and env_utils.can_join(agent, env, dest):
                return Act(ActEnum.QUEUE, [dest])

            if not agent.done():
                return Act(ActEnum.WALK, None)
        else:
            if not self.headingHome:
                homeAngle = env_utils.get_angle_from(agent.position, (env.width//2, env.height//2))
                self.headingHome = True
                return Act(ActEnum.FACE, [homeAngle])

            if not self.home:
                self.home = env_utils.get_dist(agent.position, (env.width//2, env.height//2)) <= 30
                return Act(ActEnum.WALK, None)
            
            return Act(ActEnum.IDLE)

