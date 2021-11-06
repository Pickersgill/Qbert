from kiosk import Kiosk, Queue, Server, ServerGroup
from agents import Agent, DumbMind, ActEnum, Act
from services import SEnum
from environment import Env, env_utils
from tasks import Task, TaskList
from minds import CleverMind, ClevererMind

import environment
import random

# MODIFY THESE VALUES TO CHANGE THE SIMULATION:

TIMEOUT = 0
AGENTS = 1
TASKS = 50

WIDTH = 1200
HEIGHT = 800

SERVERS = 1
SERVICE_TIME = 5

# DON'T MODIFY THE REST OF THIS FILE UNLESS YOU KNO WHAT YOU'RE DOING

names = list(n for n in open("names.txt"))

def generate_simple_env():
    simpleEnv = Env(time_limit=TIMEOUT, w=WIDTH, h=HEIGHT)
    for service in SEnum:
        simpleEnv.add_kiosk(service=service, servers=SERVERS, service_time=SERVICE_TIME)
    for service in SEnum:
        simpleEnv.add_kiosk(service=service, servers=SERVERS, service_time=SERVICE_TIME)
    
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

