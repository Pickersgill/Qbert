
class Task:
    def __init__(self, service, priority=0):
        self.service = service
        self.priority = priority
        self.complete = False

    def is_complete(self):
        return self.complete
    
    def make_complete(self):
        self.complete = True

    def __str__(self):
        return self.service.name
        

class TaskList(list):
    def __init__(self, initial_contents=[]):
        self += initial_contents

    def get_remaining(self):
        rem = TaskList()
        for task in self:
            if not task.is_complete():
                rem.append(task)
        return rem
    
    def get_complete(self):
        com = TaskList()
        for task in self:
            if task.is_complete():
                com.append(task)
        return com

    def all_complete(self):
        return len(self.get_remaining()) == 0
                
    def get_highest_priority(self, service_filter=None):
        highest = None
        for task in self.get_remaining():
            if service_filter is None or task.service in service_filter:
                if highest is None or task.priority > highest.priority:
                    highest = task

        return highest

    def empty(self):
        return len(self) == 0

    def __str__(self):
        return "Task list: [" + ", ".join(map(str, self)) + "]"
