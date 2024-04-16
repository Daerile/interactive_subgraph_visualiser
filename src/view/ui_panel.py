import pygame as pg
import pygame_gui as pgui

class UIPanel:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.manager = pgui.UIManager((width, height))
        self.base_panel = self.create_base_panel()
        self.info_label = self.create_information_box('This is an information box')

    def create_information_box(self, text):
        info_label = pgui.elements.UILabel(
            text=text,
            relative_rect=pg.Rect(0, 0, self.width, self.height),
            manager=self.manager,
            container=self.base_panel
        )
        return info_label

    def create_base_panel(self):
        base_panel = pgui.elements.UIPanel(
            relative_rect=pg.Rect(0, 0, self.width, self.height),
            starting_height=0,
            manager=self.manager,
            anchors={'left': 'left',
                     'right': 'right',
                     'top': 'top',
                     'bottom': 'bottom'}
        )
        return base_panel

    def process_events(self, event):
        self.manager.process_events(event)

    def update(self, time_delta):
        self.manager.update(time_delta)

    def draw_ui(self):
        self.manager.draw_ui(self.window)

    def get_manager(self):
        return self.manager
