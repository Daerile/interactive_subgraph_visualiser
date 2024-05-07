import pygame as pg


class NodeButton:
    font_cache = {}  # Cache to hold font objects

    @classmethod
    def get_font(cls, size):
        if size not in cls.font_cache:
            cls.font_cache[size] = pg.font.Font(None, size)
        return cls.font_cache[size]

    def __init__(self, surface, x, y, radius, node, color=(0, 92, 37), text_color=(255, 255, 255)):
        self.x = int(x)
        self.y = int(y)
        self.surface = surface
        self.radius = radius
        self.color = color
        self.node = node
        self.text = node.get_id()
        self.text_color = text_color
        self.font_size = self.calculate_font_size()
        self.font = pg.font.Font(None, self.font_size)  # Initialize font; None for default font
        self.last_click_time = 0
        self.last_click_pos = (0,0)

        self.unscaled_font_size = self.font_size
        self.unscaled_radius = radius

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

    def calculate_font_size(self):
        min_font_size = 12
        max_font_size = 30
        diameter = self.radius * 2 - 3

        # Calculate a scaling factor based on the length of the text
        length_factor = max(1, len(self.text) / 3)  # Adjust this division factor based on empirical results

        # Calculate the initial font size based on the diameter and adjusted by the length of the text
        font_size = max(min_font_size, min(max_font_size, (diameter / length_factor)))

        return int(font_size - 3)

    def draw(self):
        pg.draw.circle(self.surface, self.color, (self.x, self.y), int(self.radius))
        if self.radius > 10:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.x, self.y))
            self.surface.blit(text_surface, text_rect)

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.draw()

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.draw()

    def zoom(self, zoom_lvl, zoom_scale, zoom_center=(0, 0)):
        self.radius = self.radius * zoom_scale
        delta_x = self.x - zoom_center[0]
        delta_y = self.y - zoom_center[1]
        delta_x2 = zoom_scale * delta_x
        delta_y2 = zoom_scale * delta_y
        self.x = int(zoom_center[0] + delta_x2)
        self.y = int(zoom_center[1] + delta_y2)


        new_font_size = int(self.unscaled_font_size * zoom_scale)
        if abs(new_font_size - self.font_size) >= 3:  # Update font only on significant changes
            self.font_size = new_font_size
            self.font = self.get_font(self.font_size)

        self.draw()

    def change_colors(self, colors, selected=False, searched=False):
        if selected:
            self.color = colors['selected_node']
        elif searched:
            self.color = colors['searched_node']
        else:
            self.color = colors['node']
        self.text_color = colors['text']
        self.draw()

    def information_dict(self):
        return self.node.get_attributes()

