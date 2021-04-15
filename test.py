import unittest
from unittest import TestCase
from kiosk import Kiosk, Queue, Server, ServerGroup
from services import SEnum
from environment import Env


DEFAULT_AGENT = "agent 1"
ENV = Env()

def makeKiosk(servers=1, service_time=1, service=SEnum.GREEN):
    env = ENV
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
        

if __name__ == '__main__':
    unittest.main()
