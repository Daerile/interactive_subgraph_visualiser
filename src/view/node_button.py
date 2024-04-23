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

    def handle_click(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if (mouse_x - self.x)**2 + (mouse_y - self.y)**2 <= self.radius**2:
                return True
        return False

    def draw(self):
        pg.draw.circle(self.surface, self.color, (self.x, self.y), self.radius)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.draw()

    def information_dict(self):
        return self.node.get_attributes()
