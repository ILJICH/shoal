# coding: utf-8
"""
Application that runs the simulation of behaviour.
"""
__author__ = 'iljich'

from random import randint
from math import copysign


class Creep(object):

    world = None

    forward_acc = 1000
    rotatory_acc = 0.0005

    density = 0.2

    min_speed = 50

    def __init__(self, location, rotation, size, color):
        self.location = location
        self.rotation = rotation
        self.size = size
        self.weight = size ** 2 * self.density
        self.color = color
        self.speed = [0, 0]
        self.speed_rot = 0
        self.acceleration = 0
        self.acceleration_rot = 0
        self.target = self.location

    def move(self):
        target = self.think()
        throttle, rotation = self.go_to(target)
        self.world.creep_move(self, throttle, rotation)

    def think(self):
        x, y = self.location
        xd, yd = self.target
        if self.size ** 2 >= (x - xd) ** 2 + (y - yd) ** 2:
            self.target = [randint(200, 824), randint(200, 568)]
        return self.target

    def go_to(self, destination):
        x, y = self.location
        xv, yv = self.speed
        xd, yd = destination
        # vector of needed motion
        xr, yr = xd - x, yd - y
        # resulting vector
        xa, ya = xr - xv, yr - yv
        # if we need to speed up - a sign of cos between r and v
        # TODO: we need to do it gradually
        throttle = self.forward_acc \
            if (xa * xv + ya * yv) >= 0 \
            else self.min_speed
        # if we need to turn left - a sign of sin between r and v
        # TODO: That. Is. Wrong. Should think about something else.
        rotation = copysign(self.rotatory_acc, (xv * ya - xa * yv))

        # debugging print, yay!
        print x, y, xv, yv, xd, yd, xr, yr, \
            (xa * xv + ya * yv), (xa * yv - xv * ya)

        return throttle, rotation
