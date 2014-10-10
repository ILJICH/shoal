# coding: utf-8
"""
Application that runs the simulation of the world.
"""
__author__ = 'iljich'

from math import sin, cos, copysign

from numpy import array

from creep import Creep


class World(object):

    creeps = []

    damping_rot = 0.1

    fluid_resistance = 1

    def spawn_creep(self, *args, **kwargs):
        creep = Creep(*args, **kwargs)
        self.register_creep(creep)

    def register_creep(self, creep):
        self.creeps.append(creep)
        creep.world = self

    def creep_move(self, creep, forward_acc, rotatory_acc):
        r = array([cos(creep.rotation), sin(creep.rotation)])
        # applied force
        fa = forward_acc * r
        fr = Physics.get_drag(creep.speed, creep.size,
                              self.fluid_resistance, 0.1)
        # TODO: that needs a little bit closer model
        a = fa + fr
        creep.acceleration = a / creep.weight

        # TODO: that should also take in account the size of the creep
        rot_res = copysign(self.damping_rot * (creep.speed_rot ** 2), creep.speed_rot)
        creep.acceleration_rot += (rotatory_acc - rot_res)

    def tick(self):
        for creep in self.creeps:
            creep.speed += creep.acceleration
            creep.speed_rot += creep.acceleration_rot
            creep.location += creep.speed
            creep.rotation += creep.speed_rot


class Physics(object):

    @staticmethod
    def get_drag(v, s, p, c):
        vx, vy = v
        d = c * p * s / 2
        return array([-copysign(d * (vx ** 2), vx), -copysign(d * (vy ** 2), vy)])


class Math(object):

    @staticmethod
    def sum_vectors(*v):
        print v
        x, y = zip(*v)
        return [sum(x), sum(y)]
