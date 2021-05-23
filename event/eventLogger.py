import json

class EventLogger:

    def __init__(self):
        self.event_list = list()

    def log(self, event):
        if type(event) is not str:
            self.event_list += [event]

        
    def compile(self, dest="event_log.json"):
        events = list(e.to_dict() for e in self.event_list)
        json_str = json.dumps({"events" : events}, sort_keys=True, indent=4)

        json_dest = open(dest, "w+")
        json_dest.write(json_str)
        json_dest.close()
        
        
