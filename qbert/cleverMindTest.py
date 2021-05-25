from kiosk import Kiosk, Queue, Server, ServerGroup
from agents import Agent, DumbMind, ActEnum, Act
from services import SEnum
from environment import Env, env_utils
from tasks import Task, TaskList

import environment
import random

TIMEOUT = 1000
AGENTS = 20

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

names = list(n for n in open("names.txt"))

def generate_simple_env():
    simpleEnv = Env(time_limit=TIMEOUT, w=600, h=600)
    for service in SEnum:
        simpleEnv.add_kiosk(service=service, servers=1, service_time=5)
    
    return simpleEnv

def populate_env(env, agents=1, tasks=1):
    for i in range(1, agents + 1):
        spawn_pos = env_utils.get_random_pos(env)
        agent_name = str(i) + random.choice(names)
        new_agent = Agent(mind=CleverMind(), name=agent_name)
        env.add_agent(new_agent, spawn_pos)

        for t in range(tasks):
            env.assign_task(new_agent, Task(SEnum.random()))
    
def start(env):
    while not env.should_terminate():
        env.cycle()

    env.event_logger.compile()
    print("EVENTS GENERATED: ", len(env.event_logger.event_list))

if __name__ == '__main__':
    env = generate_simple_env()
    populate_env(env, agents=AGENTS)
    start(env)

