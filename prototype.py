# coding: utf-8
"""
This file contains code that is to be revised and split in parts later.
Purely a playground.
"""
from math import sin, pi, cos, copysign
import pyglet
from pyglet.gl import GL_TRIANGLES

__author__ = 'iljich'


class Creep(object):

    world = None

    forward_acc = 5
    rotatory_acc = 0.001

    def __init__(self, location, rotation, size):
        self.location = location
        self.rotation = rotation
        self.size = size
        self.speed = [0, 0]
        self.speed_rot = 0

    def move(self):
        throttle, rotation = self.go_to((1000, 384))
        self.world.creep_move(self, throttle, rotation)

    def go_to(self, destination):
        x, y = self.location
        xv, yv = self.speed
        xd, yd = destination
        # vector of needed motion
        xr, yr = xd - x, yd - y
        # resulting vector
        xa, ya = xr - xv, yr - yv
        # if we need to speed up - a sign of cos between r and v
        throttle = self.forward_acc if (xa * xv + ya * yv) >= 0 else 0
        # if we need to turn left - a sign of sin between r and v
        rotation = - copysign(self.rotatory_acc, (xa * yv - xv * ya))

        # debugging print, yay!
        print x, y, xv, yv, xd, yd, xr, yr, \
            (xa * xv + ya * yv), (xa * yv - xv * ya)

        return throttle, rotation


class Drawer(object):

    def draw(self, creep):
        # creep is a triangle
        x, y = creep.location
        s = creep.size
        r = creep.rotation
        pyglet.graphics.draw(
            3, GL_TRIANGLES,
            ('v2f',
             (x + s * cos(r + 0), y + s * sin(r + 0),
              x + s * cos(r + 4 * pi / 3), y + s * sin(r + 4 * pi / 3),
              x + s * cos(r + 8 * pi / 3), y + s * sin(r + 8 * pi / 3))),
            ('c3B', (150, 0, 0) * 3)
        )


class World(object):

    creeps = []

    damping_fwd = 0.1
    damping_rot = 30

    def register_creep(self, creep):
        self.creeps.append(creep)
        creep.world = self

    def creep_move(self, creep, forward_acc, rotatory_acc):
        r = creep.rotation
        creep.speed[0] += (
            forward_acc * cos(r) -
            copysign(self.damping_fwd * (creep.speed[0] ** 2), creep.speed[0])
        )
        creep.speed[1] += (
            forward_acc * sin(r) -
            copysign(self.damping_fwd * (creep.speed[1] ** 2), creep.speed[1])
        )
        creep.speed_rot += (
            rotatory_acc -
            copysign(
                self.damping_rot * (creep.speed_rot ** 2),
                creep.speed_rot
            )
        )

    def tick(self):
        for creep in self.creeps:
            creep.location[0] += creep.speed[0]
            creep.location[1] += creep.speed[1]
            creep.rotation += creep.speed_rot


window = pyglet.window.Window(1024, 768)

drawer = Drawer()
world = World()
creep = Creep([0, 0], 0, 40)
world.register_creep(creep)


def update(dt):
    window.clear()
    creep.move()
    world.tick()
    drawer.draw(creep)

pyglet.clock.schedule_interval(update, 1/60.0)


pyglet.app.run()
