import pygame as pg


class NodeButton:
    # Cache to hold font objects
    font_cache = {}

    @classmethod
    # Class method to get font of a specific size, creates and caches it if not already present
    def get_font(cls, size):
        if size not in cls.font_cache:
            cls.font_cache[size] = pg.font.Font(None, size)
        return cls.font_cache[size]

    # Constructor for the NodeButton class
    def __init__(self, surface, x, y, radius, node, color=(0, 92, 37), text_color=(255, 255, 255)):
        self.x = int(x)
        self.y = int(y)
        self.surface = surface
        self.radius = radius
        self.color = color
        self.node = node
        self.text = node.id
        self.text_color = text_color
        self.font_size = self.calculate_font_size()
        self.font = self.get_font(self.font_size)  # Initialize font
        self.last_click_time = 0
        self.last_click_pos = (0, 0)

        self.unscaled_font_size = self.font_size
        self.unscaled_radius = radius

    # Method to handle click events on the node button
    def handle_click(self, event, time):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if time - self.last_click_time <= 0.3 and event.pos == self.last_click_pos:
                self.last_click_pos = event.pos
                self.last_click_time = time
                return 2
            if (mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2 <= self.radius ** 2:
                self.last_click_pos = event.pos
                self.last_click_time = time
                return 1
        return 0

    # Method to calculate the font size based on the radius and text length
    def calculate_font_size(self):
        max_diameter = self.radius * 2
        font_size = max_diameter * 0.4  # Start with 40% of the diameter
        font = self.get_font(int(font_size))

        # Measure text width and adjust font size
        while font.size(self.text)[0] > max_diameter - 10 and font_size > 10:  # Ensure some padding
            font_size -= 1
            font = self.get_font(int(font_size))

        return int(font_size)

    # Method to draw the node button on the surface
    def draw(self):
        pg.draw.circle(self.surface, self.color, (self.x, self.y), int(self.radius))
        if self.radius > 10:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.x, self.y))
            self.surface.blit(text_surface, text_rect)

    # Method to set the position of the node button
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.draw()

    # Method to move the node button by a certain delta
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.draw()

    # Method to zoom the node button
    def zoom(self, zoom_lvl, zoom_scale, zoom_center=(0, 0)):
        self.radius = self.radius * zoom_scale
        delta_x = self.x - zoom_center[0]
        delta_y = self.y - zoom_center[1]
        delta_x2 = zoom_scale * delta_x
        delta_y2 = zoom_scale * delta_y
        self.x = int(zoom_center[0] + delta_x2)
        self.y = int(zoom_center[1] + delta_y2)

        self.font_size = self.calculate_font_size()
        self.font = self.get_font(self.font_size)

        self.draw()

    # Method to change the colors of the node button
    def change_colors(self, colors, selected=False, searched=False):
        if selected:
            self.color = colors['selected_node']
        elif searched:
            self.color = colors['searched_node']
        else:
            self.color = colors['node']
        self.text_color = colors['text']
        self.draw()

    # Method to return the attributes of the node as a dictionary
    def information_dict(self):
        return self.node.attributes
