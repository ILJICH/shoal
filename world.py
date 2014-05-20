# coding: utf-8
"""
Application that runs the simulation of the world.
"""
__author__ = 'iljich'

from math import sin, cos, copysign

from creep import Creep


class World(object):

    creeps = []

    damping_rot = 0.00001

    fluid_resistance = 25

    def spawn_creep(self, *args, **kwargs):
        creep = Creep(*args, **kwargs)
        self.register_creep(creep)

    def register_creep(self, creep):
        self.creeps.append(creep)
        creep.world = self

    def creep_move(self, creep, forward_acc, rotatory_acc):
        r = creep.rotation
        # applied force
        fa = forward_acc * cos(r), forward_acc * sin(r)
        fr = Physics.get_drag(creep.speed, creep.size,
                              self.fluid_resistance, 0.1)
        # TODO: that needs a little bit closer model
        a = Math.sum_vectors(fa, fr)
        creep.acceleration = a[0] / creep.weight, a[1] / creep.weight

        # TODO: that should also take in account the size of the creep
        rot_res = self.damping_rot * (creep.speed[0] ** 2 +
                                      creep.speed[1] ** 2)
        creep.acceleration_rot = (rotatory_acc - rot_res)

    def tick(self):
        for creep in self.creeps:
            creep.speed[0] += creep.acceleration[0]
            creep.speed[1] += creep.acceleration[1]
            creep.speed_rot += creep.acceleration_rot
            creep.location[0] += creep.speed[0]
            creep.location[1] += creep.speed[1]
            creep.rotation += creep.speed_rot


class Physics(object):

    @staticmethod
    def get_drag(v, s, p, c):
        vx, vy = v
        d = c * p * s / 2
        return [-copysign(d * (vx ** 2), vx), -copysign(d * (vy ** 2), vy)]


class Math(object):

    @staticmethod
    def sum_vectors(*v):
        print v
        x, y = zip(*v)
        return [sum(x), sum(y)]

    @staticmethod
    def add_vectors(v1, *v):
        x, y = zip(*v)
        v1[0] += sum(x)
        v1[1] += sum(y)
