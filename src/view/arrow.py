import pygame as pg
import pygame_gui as pgui


class Arrow:
    def __init__(self, window, positions, node_start, node_end, color=(0, 0, 0), size=2, arrowhead_size=10):
        self.window = window
        self.positions = positions
        self.color = color
        self.size = size
        self.arrowhead_size = arrowhead_size
        self.node_start = node_start
        self.node_end = node_end

        self.unzoomed_positions = positions
        self.unzoomed_size = size
        self.unzoomed_arrowhead_size = arrowhead_size

    def draw(self):
        start, end = self.positions[0]
        pg.draw.line(self.window, self.color, start, end, self.size)

        start, end = self.positions[1]
        pg.draw.line(self.window, self.color, start, end, self.arrowhead_size)

        start, end = self.positions[2]
        pg.draw.line(self.window, self.color, start, end, self.arrowhead_size)

    def zoom(self, zoom_scale):
        new_positions = []
        for (start, end) in self.unzoomed_positions:
            new_positions.append(
                ((int(start[0] * zoom_scale), int(start[1] * zoom_scale)),
                 (int(end[0] * zoom_scale), int(end[1] * zoom_scale)))
            )
        self.positions = new_positions
        self.size = int(self.unzoomed_size * zoom_scale)
        self.arrowhead_size = int(self.unzoomed_arrowhead_size * zoom_scale)
        self.draw()

    def move(self, dx, dy):
        new_positions = []
        for (start, end) in self.positions:
            new_positions.append(((start[0] + dx, start[1] + dy), (end[0] + dx, end[1] + dy)))
        self.positions = new_positions
        self.draw()
