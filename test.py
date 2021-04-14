import unittest
from unittest import TestCase
from kiosk import Kiosk, Queue
from services import SEnum


class KioskTest(TestCase):

    def testKioskExists(self):
        self.assertTrue(Kiosk(1, 1, 1, SEnum.GREEN) is not None)

    def testQueueExists(self):
        self.assertTrue(Queue() is not None)

    def testQueuePut(self):
        q = Queue()
        q.put("agent 1")

    def testQueueGet(self):
        q = Queue()
        q.put("agent 1")
        q.get()

    def testEnqueueAgent(self):
        k = Kiosk(1, 5, 1, SEnum.GREEN)
        k.enqueueAgent("agent 1")

if __name__ == '__main__':
    unittest.main()
