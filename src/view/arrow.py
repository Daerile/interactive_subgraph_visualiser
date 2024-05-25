import pygame as pg


class Arrow:
    """
    This class represents an arrow in a graphical user interface.
    """

    def __init__(self, window, button_start, button_end, color=(136, 136, 136), size=2, arrowhead_size=10):
        """
        Initialize an Arrow object with the given parameters.
        """
        self.window = window
        self.color = color
        self.size = size
        self.arrowhead_size = arrowhead_size
        self.button_start = button_start
        self.button_end = button_end

        self.unzoomed_size = size
        self.unzoomed_arrowhead_size = arrowhead_size

    def draw(self):
        """
        Draw the arrow on the window.
        """
        start, end = (self.button_start.x, self.button_start.y), (self.button_end.x, self.button_end.y)
        pg.draw.line(self.window, self.color, start, end, self.size)

    def zoom(self, zoom_scale):
        """
        Zoom the arrow based on the given zoom scale.
        """
        self.size = int(self.unzoomed_size * zoom_scale) if self.unzoomed_size * zoom_scale > 1 else 1
        self.arrowhead_size = int(
            self.unzoomed_arrowhead_size * zoom_scale) if self.unzoomed_arrowhead_size * zoom_scale > 1 else 1
        self.draw()

    def change_color(self, color):
        """
        Change the color of the arrow to the given color.
        """
        self.color = color
        self.draw()

    def handle_click(self, event):
        """
        Handle a mouse click event. If the click is on the arrow, return 1. Otherwise, return 0.
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            num = abs((self.button_end.y - self.button_start.y) * mouse_x - (
                        self.button_end.x - self.button_start.x) * mouse_y + self.button_end.x * self.button_start.y - self.button_end.y * self.button_start.x)
            den = ((self.button_end.y - self.button_start.y) ** 2 + (
                        self.button_end.x - self.button_start.x) ** 2) ** 0.5
            if den == 0:
                return 0
            distance = num / den
            dot_product = (mouse_x - self.button_start.x) * (self.button_end.x - self.button_start.x) + (
                        mouse_y - self.button_start.y) * (self.button_end.y - self.button_start.y)
            if dot_product < 0 or dot_product > (self.button_end.x - self.button_start.x) ** 2 + (
                    self.button_end.y - self.button_start.y) ** 2:
                return 0
            if distance <= 4:
                return 1
        return 0
