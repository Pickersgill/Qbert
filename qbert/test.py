import unittest
from unittest import TestCase
from kiosk import Kiosk, Queue, Server, ServerGroup
from agents import Agent
from services import SEnum
from environment import Env
from tasks import Task, TaskList


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


class TaskTest(TestCase):

    def testTaskExists(self):
        try:
            print("TESTING")
            self.assertTrue(Task(SEnum.GREEN, priority=1) is not None)
        except:
            print("PROBLEM DURING TEST")

    def testTaskListExists(self):
        print("TESTING")
        TaskList([Task(SEnum.GREEN, priority=1)])
    
    def testTaskCompletion(self):
        agent = Agent()
        agent.completeTask(SEnum.GREEN)
        agent.assignTask(Task(SEnum.GREEN))
        agent.completeTask(SEnum.GREEN)


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
        
    def testManyWalkToKiosk(self):
        newEnv = Env()
        newEnv.addKiosk(service=SEnum.GREEN, servers=1, service_time=5, position=100)
        newEnv.addKiosk(service=SEnum.BLUE, servers=1, service_time=5, position=150)
        agent1 = Agent(name="ryan")
        agent1.assignTask(Task(SEnum.GREEN))
        newEnv.addAgent(agent1, (100, 100))
        agent2 = Agent(name="todd")
        agent2.assignTask(Task(SEnum.BLUE))
        newEnv.addAgent(agent2, (150, 100))
    
        old1 = agent1.tasks.allComplete()
        old2 = agent2.tasks.allComplete()

        while not newEnv.shouldTerminate():
            print("tick", newEnv.time)
            newEnv.cycle()
        
        print(old1, agent1.tasks.allComplete())
        print(old2, agent2.tasks.allComplete())

if __name__ == '__main__':
    unittest.main()


