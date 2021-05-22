from enum import Enum

class ActEnum(Enum):
    WALK = 1
    RUN = 2
    FACE = 3
    QUEUE = 4
    
class Act:
    def __init__(self, act_type, args):
        self.act_type = act_type
        self.args = args

