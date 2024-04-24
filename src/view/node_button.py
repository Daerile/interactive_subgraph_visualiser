import pygame as pg


class NodeButton:
    def __init__(self, surface, x, y, radius, node, color=(0, 0, 0)):
        self.x = int(x)
        self.y = int(y)
        self.surface = surface
        self.radius = radius
        self.color = color
        self.node = node
        self.text = node.get_id()  # assuming get_id() returns a string
        self.last_click_time = 0
        self.last_click_pos = (0,0)

        self.unscaled_radius = radius
        self.unscaled_x = x
        self.unscaled_y = y

    def handle_click(self, event, time):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if time - self.last_click_time <= 0.3 and event.pos == self.last_click_pos:
                self.last_click_pos = event.pos
                self.last_click_time = time
                return 2
            if (mouse_x - self.x)**2 + (mouse_y - self.y)**2 <= self.radius**2:
                self.last_click_pos = event.pos
                self.last_click_time = time
                return 1
        return 0

    def draw(self):
        pg.draw.circle(self.surface, self.color, (self.x, self.y), self.radius)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.draw()

    def zoom(self, zoom_scale):
        self.x = int(self.unscaled_x * zoom_scale)
        self.y = int(self.unscaled_y * zoom_scale)
        self.radius = int(self.unscaled_radius * zoom_scale)
        self.draw()

    def information_dict(self):
        return self.node.get_attributes()

