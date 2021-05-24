from kiosk import Kiosk
from agents import ActEnum
from event import EventLogger

import environment
import random
import math

def num_to_perimeter(env, num):
    w = env.width
    h = env.height

    if num is None:
        return num_to_perimeter(env, random.randint(0, w + w + h + h))

    num = num % (w + w + h + h)
    if num <= w:
        x = num
        y = 0
    elif num <= w + h:
        x = w
        y = num % w
    elif num <= w + w + h:
        x = w - num % (w + h)
        y = h
    elif num <= w + w + h + h:
        x = 0
        y = h - num % (w + w + h)

    return (x, y)

def get_random_pos(env):
    return (random.randint(0, env.width), random.randint(0, env.height))

def get_nearest_kiosk(agent, env, service_filter=None):
    near_dist = -1
    near = None
    for kiosk in env.kiosks:
        if service_filter is None or kiosk.service in service_filter:
            c_dist = get_dist(agent.position, kiosk.entrance)
            if c_dist <= near_dist or near_dist == -1:
                near_dist = c_dist
                near = kiosk

    return near

def get_angle_from(pos1, pos2):
    angle = (math.atan2(pos2[0] - pos1[0], pos1[1] - pos2[1]) * 180 / math.pi)
    if angle < 0:
        angle += 360
    return angle
    

def get_dist(pos1, pos2):
    xdif = abs(pos1[0] - pos2[0])
    ydif = abs(pos1[1] - pos2[1])
    return math.sqrt(xdif * xdif + ydif * ydif)

def can_join(agent, env, kiosk):
    return get_dist(agent.position, kiosk.entrance) <= environment.ENTRANCE_SIZE
        
