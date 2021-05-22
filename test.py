import unittest
from unittest import TestCase
from kiosk import Kiosk, Queue, Server, ServerGroup
from agents import Agent
from services import SEnum
from environment import Env


DEFAULT_AGENT = Agent()
ENV = Env()

def makeKiosk(servers=1, service_time=1, service=SEnum.GREEN, env=ENV):
    return Kiosk(env, service, servers, service_time)

class KioskTest(TestCase):

    def testKioskExists(self):
        self.assertTrue(makeKiosk() is not None)

    def testQueueExists(self):
        self.assertTrue(Queue() is not None)

    def testQueuePut(self):
        q = Queue()
        q.put(DEFAULT_AGENT)

    def testQueueGet(self):
        q = Queue()
        q.put(DEFAULT_AGENT)
        q.pop()

    def testEnqueueAgent(self):
        k = makeKiosk()
        k.enqueue_agent(DEFAULT_AGENT)

    def testServerFramework(self):
        k = makeKiosk()
        sg = ServerGroup(k)
        s = Server(sg)
        s.serve(DEFAULT_AGENT)
        self.assertTrue(not s.free)
        s.tick()
        s.tick()
        s.tick()
        self.assertTrue(s.free)

    def testServeAgents(self):
        k = makeKiosk(service_time=2)
        k.enqueue_agent(DEFAULT_AGENT)
        k.enqueue_agent(DEFAULT_AGENT)
        k.tick()
        k.tick()
        self.assertTrue(len(k.queue) == 1)
        k.tick()
        k.tick()
        self.assertTrue(len(k.queue) == 0)

class AgentTest(TestCase):
    def testAgentExist(self):
        self.assertTrue(Agent() is not None)

class EnvironmentTest(TestCase):

    def testEnvExists(self):
        self.assertTrue(Env() is not None)

    def testAddKioskEnv(self):
        newEnv = Env()
        newEnv.addKiosk(service=SEnum.GREEN, servers=1, service_time=1, position=50)
        ''' Add a new Kiosk to the environment '''

    def testAddAgentEnv(self):
        newEnv = Env()
        newEnv.addAgent(DEFAULT_AGENT, (100, 100))
        
    def testTickEnv(self):
        newEnv = Env()
        newEnv.tick()
        ''' Perform 1 tick in the environment '''

    def testAgentCycleEnv(self):
        newEnv = Env()
        agent = Agent()
        newEnv.addAgent(agent, (100, 100))
        newEnv.tick()

    def testDecideEnv(self):
        newEnv = Env()
        agent = Agent()
        agent.facing = 45
        newEnv.addAgent(agent, (100, 100))
        newEnv.decide()
        newEnv.decide()
        
    def testWalkToKiosk(self):
        newEnv = Env()
        newEnv.addKiosk(service=SEnum.GREEN, servers=1, service_time=5, position=100)
        agent = Agent()
        newEnv.addAgent(agent, (100, 100))

        for i in range(100):
            print("tick", i)
            newEnv.cycle()
        

if __name__ == '__main__':
    unittest.main()
