from enum import Enum

import random

class ServiceEnum(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    ORANGE = 5
    PURPLE = 6

    @classmethod
    def random(cls):
        return random.choice(list(ServiceEnum))

