import matplotlib.pyplot as plt
from body import Body, BodyType
from typing import List
import time


class TerrainWindow:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(0, height)
        self.points = {}

        self.ax.set_aspect('equal', adjustable='box')



    def add_point(self, x, y, color='blue', opacity=1.0):
        point = self.ax.scatter(x, y, color=color, alpha=opacity)
        self.points[(x, y)] = point

    def update_map(self, points: List[Body], color='blue', opacity=-1.0):
        self.remove_everything()
        for point in points:
            p = point.get2DPos()

            match point.getType():
                case BodyType.FIXED_MARKER:
                    color = 'green'
                case BodyType.TARGET:
                    color = 'red'
                case BodyType.MOVABLE_BODY:
                    color = 'purple'
                case BodyType.CONNECTED_BODY:
                    color = 'orange'

            if opacity == -1.0:
                opacity = 1 - 0.1*(time.time() - point.lastSeen)
                if opacity < 0.2:
                    opacity = 0.2

            self.add_point(p[0], p[1], color=color, opacity=opacity)

    def move_point(self, old_x, old_y, new_x, new_y):
        if (old_x, old_y) in self.points:
            point = self.points[(old_x, old_y)]
            point.set_offsets([new_x, new_y])
            self.points[(new_x, new_y)] = point
            del self.points[(old_x, old_y)]


    def remove_everything(self):
        for point in self.points.values():
            point.remove()
        self.points = {}

    def remove_point(self, x, y):
        if (x, y) in self.points:
            point = self.points[(x, y)]
            point.remove()
            del self.points[(x, y)]

    def change_color(self, x, y, color):
        if (x, y) in self.points:
            point = self.points[(x, y)]
            point.set_color(color)

    def change_opacity(self, x, y, opacity):
        if (x, y) in self.points:
            point = self.points[(x, y)]
            point.set_alpha(opacity)

    def show(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
