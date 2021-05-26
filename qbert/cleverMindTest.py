from kiosk import Kiosk, Queue, Server, ServerGroup
from agents import Agent, DumbMind, ActEnum, Act
from services import SEnum
from environment import Env, env_utils
from tasks import Task, TaskList
from minds import CleverMind, ClevererMind

import environment
import random

TIMEOUT = 3000
AGENTS = 50
TASKS = 5

names = list(n for n in open("names.txt"))

def generate_simple_env():
    simpleEnv = Env(time_limit=TIMEOUT, w=600, h=600)
    for service in SEnum:
        simpleEnv.add_kiosk(service=service, servers=1, service_time=5)
    
    return simpleEnv

def populate_env(env, agents=1, tasks=1, mind=CleverMind):
    for i in range(1, agents + 1):
        spawn_pos = env_utils.get_random_pos(env)
        agent_name = str(i) + random.choice(names)
        new_agent = Agent(mind=mind(), name=agent_name)
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
    populate_env(env, agents=AGENTS, tasks=TASKS, mind=ClevererMind)
    start(env)

