import pygame


class NodeButton:
    def __init__(self, surface, x, y, radius, node, color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.node = node
        self.circle = pygame.draw.circle(surface, color, (x, y), radius)
        self.text = node.get_id()  # assuming get_id() returns a string

    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if (mouse_x - self.x)**2 + (mouse_y - self.y)**2 <= self.radius**2:
                print('clicked on', self.text)
                return True
        return False
