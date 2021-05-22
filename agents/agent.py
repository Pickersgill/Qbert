from .actEnum import ActEnum, Act

class DumbMind:
    def __init__(self):
        self.turned = False
        pass

    def decide(self, agent, env):

        if env.time >= 94:
            if self.turned:
                return Act(ActEnum.WALK, None)
            else:
                self.turned = True
                return Act(ActEnum.FACE, [180])
    
        elif env.time % 2 == 0:
            return Act(ActEnum.WALK, None)
        else:
            return Act(ActEnum.QUEUE, None) 

dm = DumbMind()

class Agent:
    def __init__(self, mind=None):
        self.mind = mind
        self.queueing = False
        self.position = (0, 0)
        self.facing = 0
        self.tasks = list()
        pass

    def tick(self):
        pass

    def decide(self, env):
        if self.mind is not None:
            return self.mind.decide(self, env)
        else:
            return dm.decide(self, env)

    def setPosition(self, newpos):
        self.position = newpos

    def __str__(self):
        r = f"AGENT AT POSITION {self.position} " 
        r += f"FACING {self.facing} "
        r +=  f"WITH {len(self.tasks)} TASKS REMAINING."
        return r


        
