# coding: utf-8
"""
This file contains code that is to be revised and split in parts later.
Purely a playground.
"""
from math import sin, pi, cos, copysign, sqrt
from random import randint
import pyglet
from pyglet.gl import GL_TRIANGLES, GL_POINTS

__author__ = 'iljich'


class Creep(object):

    world = None

    forward_acc = 3
    rotatory_acc = 0.0005

    min_speed = 1

    def __init__(self, location, rotation, size, color):
        self.location = location
        self.rotation = rotation
        self.size = size
        self.color = color
        self.speed = [0, 0]
        self.speed_rot = 0
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
        rotation = copysign(self.rotatory_acc, (xv * ya - xa * yv))

        # debugging print, yay!
        print x, y, xv, yv, xd, yd, xr, yr, \
            (xa * xv + ya * yv), (xa * yv - xv * ya)

        return throttle, rotation


class Drawer(object):

    def tick(self, creeps):
        for creep in creeps:
            self.draw(creep)
            self._draw_target(creep)

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
            ('c3B', creep.color * 3)
        )

    def _draw_target(self, creep):
        pyglet.graphics.draw(
            1, GL_POINTS,
            ('v2f', creep.target),
            ('c3B', creep.color)
        )


class World(object):

    creeps = []

    damping_fwd = 0.1
    damping_rot = 0.000001

    def spawn_creep(self, *args, **kwargs):
        creep = Creep(*args, **kwargs)
        self.register_creep(creep)

    def register_creep(self, creep):
        self.creeps.append(creep)
        creep.world = self

    def creep_move(self, creep, forward_acc, rotatory_acc):
        r = creep.rotation
        # applied force
        fax, fay = forward_acc * cos(r), forward_acc * sin(r)
        frx = copysign(self.damping_fwd * (creep.speed[0] ** 2), creep.speed[0])
        fry = copysign(self.damping_fwd * (creep.speed[1] ** 2), creep.speed[1])
        # TODO: that needs a little bit closer model
        creep.speed[0] += (fax - frx)
        creep.speed[1] += (fay - fry)

        rot_res = self.damping_rot * sqrt(creep.speed[0] ** 2 + creep.speed[1] ** 2)
        creep.speed_rot += (rotatory_acc - rot_res)

    def tick(self):
        for creep in self.creeps:
            creep.location[0] += creep.speed[0]
            creep.location[1] += creep.speed[1]
            creep.rotation += creep.speed_rot


window = pyglet.window.Window(1024, 768)

world = World()
drawer = Drawer()
world.spawn_creep([10, 10], 0.1, 40, (250, 25, 25))
world.spawn_creep([1000, 10], 2, 40, (25, 250, 25))
world.spawn_creep([10, 700], 6, 40, (25, 25, 250))


def update(dt):
    window.clear()
    for creep in world.creeps:
        creep.move()
    world.tick()
    drawer.tick(world.creeps)

pyglet.clock.schedule_interval(update, 1/60.0)


pyglet.app.run()
