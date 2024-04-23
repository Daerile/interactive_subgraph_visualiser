import pygame as pg
import pygame_gui as pgui


class UIHeader:
    def __init__(self, window, manager, width, height, digraph):
        self.window = window
        self.width = width
        self.height = height
        self.manager = manager
        self.digraph = digraph
        self.base_panel = self.create_base_panel()
        self.create_buttons()

    def create_buttons(self):
        button_width = 100
        button_height = self.height - 10
        button_spacing = 10
        # Calculate starting x position so buttons are aligned
        start_x = 10  # Start 10 pixels from the left of the panel

        self.load_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(start_x, 5, button_width, button_height),
            text='Load',
            manager=self.manager,
            container=self.base_panel)

        start_x += button_width + button_spacing  # Move right for the next button

        self.save_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(start_x, 5, button_width, button_height),
            text='Save',
            manager=self.manager,
            container=self.base_panel)

        start_x += button_width + button_spacing

        self.help_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(start_x, 5, button_width, button_height),
            text='Help',
            manager=self.manager,
            container=self.base_panel)

        start_x += button_width + button_spacing

        self.options_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(start_x, 5, button_width, button_height),
            text='Options',
            manager=self.manager,
            container=self.base_panel)

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

    def killall(self):
        self.load_button.kill()
        self.save_button.kill()
        self.help_button.kill()
        self.options_button.kill()
        self.base_panel.kill()

    def process_events(self, event):
        self.manager.process_events(event)

    def draw_ui(self):
        self.manager.draw_ui(self.window)

    def get_manager(self):
        return self.manager

    def update(self, time_delta):
        self.manager.update(time_delta)
