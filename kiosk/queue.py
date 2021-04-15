

class EmptyQueueException(Exception):
    def __init__(self, message="Attempt to pop from empty queue"):
        super().__init__(message)

class Queue:

    def __init__(self):
        self.q = list()

    def pop(self):
        if self.q:
            return self.q.pop()
        else:
            raise EmptyQueueException

    def put(self, agent):
        self.q = [agent] + self.q

    def __str__(self):
        return "".join(((str(a) + "\n") for a in self.q))

    def __len__(self):
        return len(self.q)
