import json

class EventLogger:

    def __init__(self, w=200, h=200, time=1000):
        self.env_dict = {"width" : w, "height" : h, "time_limit" : time}
        self.event_list = list()

    def log(self, event):
        if type(event) is not str:
            self.event_list += [event]
        
    def compile(self, dest="event_log.json"):
        events = list(e.to_dict() for e in self.event_list)

        json_str = json.dumps({"env" : self.env_dict, "events" : events}, sort_keys=True)

        json_dest = open(dest, "w+")
        json_dest.write(json_str)
        json_dest.close()
        
        
