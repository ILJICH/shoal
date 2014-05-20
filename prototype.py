# coding: utf-8
"""
This file contains code that is to be revised and split in parts later.
Purely a playground.
"""
from math import sin, pi, cos

import pyglet
from pyglet.gl import GL_TRIANGLES, GL_POINTS

from world import World

__author__ = 'iljich'


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
