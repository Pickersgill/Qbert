

class EmptyQueueException(Exception):
    def __init__(self, message="Attempt to pop from empty queue"):
        super().__init__(message)

class Queue:

    def __init__(self):
        self.q = list()

    def get(self):
        if list:
            return self.q.pop()
        else:
            raise EmptyQueueException

    def put(self, agent):
        self.q = [agent] + self.q

    def __str__(self):
        return ((str(a) + "\n") for a in self.q)
