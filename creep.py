# coding: utf-8
"""
Application that runs the simulation of behaviour.
"""
import functools
from math import cos, sin, acos
from numpy.linalg import linalg

__author__ = 'iljich'

from random import randint

from numpy import array, dot, cross


class Creep(object):

    world = None

    forward_acc = 1000
    rotatory_acc = 0.0008

    density = 0.2

    rotation_prediction = 10

    def __init__(self, location, rotation, size, color):
        self.location = array(location)
        self.rotation = rotation
        self.size = size
        self.weight = size ** 2 * self.density
        self.color = color
        self.speed = array([0, 0])
        self.speed_rot = 0
        self.acceleration = 0
        self.acceleration_rot = 0
        self.target = self.location

    def move(self):
        target = self.think()
        throttle, rotation = self.go_to(target)
        self.world.creep_move(self, throttle, rotation)

    def think(self):
        if self.size >= linalg.norm(self.target - self.location):
            self.target = array([randint(200, 824), randint(200, 568)])
        return self.target

    def go_to(self, destination):
        p = self.location
        d = destination
        h = array([cos(self.rotation), sin(self.rotation)])

        # vector of the needed motion
        r = d - p

        length = (linalg.norm(r) * linalg.norm(h))
        cosd = cross(h, r) / length
        sind = dot(h, r) / length
        # we can't go backwards
        if sind < 0:
            sind = 0

        # taking rotation speed in account
        #acos(cosd)

        throttle = self.forward_acc * sind
        rotation = self.rotatory_acc * cosd

        # debugging print, yay!
        print p, d, r, h, sind, cosd, acos(cosd), self.speed_rot, throttle, rotation > 0

        return throttle, rotation
