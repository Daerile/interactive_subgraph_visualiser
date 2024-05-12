import pygame as pg
import pygame_gui as pgui


class UIHeader:
    def __init__(self, window, manager, width, height, digraph):
        self.window = window
        self.width = width
        self.height = height
        self.manager = manager
        self.digraph = digraph
        self.menu_points = None
        self.menu_buttons = None
        self.text_box = None
        self.base_panel = self.create_base_panel()
        self.create_buttons()
        self.popup = None

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

    # Define the handle_help_button_pressed function
    def handle_help_button_pressed(self):
        # Create a popup window
        self.popup = pgui.elements.UIWindow(
            rect=pg.Rect(0, 0, 800, 800),
            manager=self.manager,
            window_display_title='Help menu'
        )

        # Create a left panel inside the popup
        left_panel = pgui.elements.UIPanel(
            relative_rect=pg.Rect(0, 0, 200, 800),
            starting_height=0,
            manager=self.manager,
            container=self.popup,
            anchors={'left': 'left',
                     'right': 'left',
                     'top': 'top',
                     'bottom': 'bottom'}
        )

        # List of menu points with commas separating them
        self.menu_points = {
            'Welcome': '<b>Welcome to the help menu!</b><br> Here you can find all the information you need to use the application.',
            'Load a graph': '<b>Load a graph</b><br> To load a graph, click the Load button in the header.<br> You will be prompted to select a csv file with the graph data.',
            'Save a graph': '<b>Save a graph</b><br> To save a graph, click the Save button in the header.<br> You will be prompted to select a location to save the graph data.<br> You can only save graphs that are focused on a specific node.<br> If you try to save a full graph, nothing will happen.',
            'Select a node': '<b>Select a node</b><br> To select a node, click on it.<br> The node will be highlighted and it will be selected in the search panel<br><br> Otherwise, you can use the search panel to find a node by its id.',
            'Focus on a node': '<b>Focus on a node</b><br> To focus on a node, select it and click the Focus button in the search panel.<br> The graph will be centered around the selected node and only its connections will be shown.<br><br> Otherwise, you can double click on a node on the screen, and it will have the same effect.<br> By changing the depth in the search panel, you can control how many levels of connections are shown.<br> You can return to the full graph by clicking the Return button in the panel.',
            'Search box': '<b>Search box</b><br> The search box allows you to search for a node by its id.<br> You can also focus on a node by selecting it and clicking the Focus button.<br> The Return button will return you to the full graph.',
            'Edit box': '<b>Edit box</b><br>',
            'Node attributes': '<b>Node attributes</b><br> You can view the attributes of a node by selecting it.<br> The attributes will be shown in the edit box.<br> You can also edit the attributes of a node by changing the values in the edit box and clicking the Save button.',
            'Interacting with the graph': '<b>Interacting with the graph</b><br> You can move the graph by clicking and dragging on the background.<br> You can zoom in and out by scrolling with the mouse wheel.<br> You can also zoom in and out by holding the Ctrl key and scrolling with the mouse wheel.<br> You can pan the graph by holding the Shift key and dragging with the mouse.<br> You can reset the zoom and pan by pressing the R key.<br> You can change the colors of the graph by selecting a color scheme in the search panel.<br> You can also change the colors of the graph by clicking the Change colors button in the header.',
        }

        # Loop through menu points and create buttons one below another
        self.menu_buttons = {}
        for i, point in enumerate(self.menu_points.keys()):
            button = pgui.elements.UIButton(
                # Calculate vertical position based on the index
                relative_rect=pg.Rect(0, i * 50, 200, 50),
                text=point,
                manager=self.manager,
                container=left_panel
            )

            self.menu_buttons[point] = button

        # Create a right panel inside the popup
        right_panel = pgui.elements.UIPanel(
            relative_rect=pg.Rect(200, 0, 600, 800),  # Starts at x=200, spans 600 wide
            starting_height=0,
            manager=self.manager,
            container=self.popup,
            anchors={
                'left': 'left',  # This should be 'left' to anchor the left side correctly
                'right': 'right',
                'top': 'top',
                'bottom': 'bottom'
            }
        )

        # Create a text box inside the right panel
        self.text_box = pgui.elements.UITextBox(
            relative_rect=pg.Rect(0, 0, 600, 800),
            html_text=self.menu_points['Welcome'],
            manager=self.manager,
            container=right_panel
        )

        self.popup.set_blocking(True)

    def handle_menu_button_pressed(self, button):
        # Get the text of the button that was pressed
        text = button.text

        # Get the corresponding text from the menu_points dictionary
        menu_text = self.menu_points[text]

        # Set the text of the text box in the right panel
        self.text_box.set_text(menu_text)

    def killall(self):
        self.load_button.kill()
        self.save_button.kill()
        self.help_button.kill()
        self.base_panel.kill()

    def process_events(self, event):
        self.manager.process_events(event)

    def draw_ui(self):
        self.manager.draw_ui(self.window)

    def get_manager(self):
        return self.manager

    def update(self, time_delta):
        self.manager.update(time_delta)
