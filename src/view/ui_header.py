import pygame as pg
import pygame_gui as pgui
import os

# UIHeader class is responsible for creating and managing the header of the user interface.
class UIHeader:
    # Initialize the UIHeader with the given parameters.
    def __init__(self, window, manager, width, height, digraph):
        self.window = window
        self.width = width
        self.height = height
        self.manager = manager
        self.digraph = digraph
        self.menu_points = None
        self.menu_buttons = None
        self.text_box = None
        self.base_panel = self.create_base_panel()  # Create the base panel
        self.create_buttons()  # Create the buttons
        self.popup = None
        self.load_popup = None
        self.load_popup_items = None

    # Create the buttons for the UIHeader.
    def create_buttons(self):
        # Define the dimensions and spacing for the buttons.
        button_width = 100
        button_height = self.height - 10
        button_spacing = 10
        # Calculate starting x position so buttons are aligned
        start_x = 10  # Start 10 pixels from the left of the panel

        # Create the Load button.
        self.load_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(start_x, 5, button_width, button_height),
            text='Load',
            manager=self.manager,
            container=self.base_panel)

        # Move right for the next button
        start_x += button_width + button_spacing

        # Create the Save button.
        self.save_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(start_x, 5, button_width, button_height),
            text='Save',
            manager=self.manager,
            container=self.base_panel)

        # Move right for the next button
        start_x += button_width + button_spacing

        # Create the Help button.
        self.help_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(start_x, 5, button_width, button_height),
            text='Help',
            manager=self.manager,
            container=self.base_panel)

    # Create the base panel for the UIHeader.
    def create_base_panel(self):
        base_panel = pgui.elements.UIPanel(
            relative_rect=pg.Rect((0, 0), (self.width, self.height)),
            starting_height=0,
            manager=self.manager,
            margins={'left': 0, 'right': 0, 'top': 0, 'bottom': 0},
            anchors={'left': 'left',
                     'right': 'right',
                     'top': 'top',
                     'bottom': 'bottom'}
        )
        return base_panel

    # Handle the event of the Help button being pressed.
    def handle_help_button_pressed(self):
        # Create a popup window for the Help menu.
        self.popup = pgui.elements.UIWindow(
            rect=pg.Rect(0, 0, 800, 800),
            manager=self.manager,
            window_display_title='Help menu'
        )

        # Create a left panel inside the popup for the Help menu.
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
        relative_path = "view/assets"
        absolute_path = os.path.abspath(relative_path)
        print(absolute_path)
        load_a_graph_text = "<b>Load a graph</b><br> To load a graph, click the Load button in the header.<br>"
        load_a_graph_text += f'<img src = {absolute_path + "/load_button.jpg"}><br>'
        load_a_graph_text += "You will be prompted to select a csv file with the graph data."
        load_a_graph_text += f'<br><img src = {absolute_path + "/load_popup.jpg"}><br>'
        load_a_graph_text += "You will then be prompted to pair the row names.<br>"
        load_a_graph_text += "Every row that's not paired will be in the 'other' category.<br>"
        load_a_graph_text += "Please don't leave any required columns empty.<br>"
        load_a_graph_text += "Please don't pair the same column twice.<br>"
        load_a_graph_text += "If you do, the Okay button will be disabled.<br>"
        load_a_graph_text += f'<img src = {absolute_path + "/column_pair.jpg"}><br>'

        save_a_graph_text = "<b>Save a graph</b><br> To save a graph, click the Save button in the header.<br>"
        save_a_graph_text += f'<img src = {absolute_path + "/save_button.jpg"}><br>'
        save_a_graph_text += "You will be prompted to select a location to save the graph data.<br>"
        save_a_graph_text += "You can only save graphs that are focused on a specific node.<br>"
        save_a_graph_text += "If you try to save a full graph, nothing will happen.<br>"
        save_a_graph_text += f'<img src = {absolute_path + "/save_popup.jpg"}><br>'

        select_a_node_text = "<b>Select a node</b><br> To select a node, click on it.<br> The node will be highlighted and it will be selected in the search panel.<br>"
        select_a_node_text += "Otherwise, you can use the search panel to find a node by its id or click the search by name button to search by name."
        select_a_node_text += f'<img src = {absolute_path + "/select_node.jpg"}><br>'

        focus_on_a_node_text = "<b>Focus on a node</b><br> To focus on a node, select it and click the Focus button in the search panel.<br>"
        focus_on_a_node_text += f'<img src = {absolute_path + "/focus_node.jpg"}><br>'
        focus_on_a_node_text += "The graph will be centered around the selected node and only its connections will be shown.<br>"
        focus_on_a_node_text += "Otherwise, you can double click on a node on the screen, and it will have the same effect.<br>"
        focus_on_a_node_text += "By changing the depth in the search panel, you can control how many levels of connections are shown.<br>"
        focus_on_a_node_text += "By changing the horizontal and vertical spacing in the search panel, you can control the spacing between nodes.<br>"
        focus_on_a_node_text += f'<img src = {absolute_path + "/focus_variables.jpg"}><br>'
        focus_on_a_node_text += "You can return to the full graph by clicking the Return button in the panel."
        focus_on_a_node_text += f'<img src = {absolute_path + "/focused_view.jpg"}><br>'

        search_box_text = "<b>Search box</b><br> The search box allows you to search for a node by its id or name.<br>"
        search_box_text += "You can also focus on a node by selecting it and clicking the Focus button.<br>"
        search_box_text += "You can change what to search for by clicking the search by name button or search by id button.<br>"
        search_box_text += f'<img src = {absolute_path + "/search_box.jpg"}><br>'
        search_box_text += "The search box always holds the nodes visible. So if you are in focused view, you can only see the focused nodes in the search box."

        edit_box_text = "<b>Edit box</b><br>"
        edit_box_text += "In the edit box, you can change the appearance of the graph.<br>"
        edit_box_text += "With clicking dark mode or light mode, you can change the appearance of the graph.<br>"
        edit_box_text += f'<img src = {absolute_path + "/focused_view.jpg"}><br>'
        edit_box_text += f'<img src = {absolute_path + "/dark_mode.jpg"}><br>'
        edit_box_text += "With providing rgb values, you can change the following attributes:<br>"
        edit_box_text += "background color<br>"
        edit_box_text += "node color<br>"
        edit_box_text += "edge color<br>"
        edit_box_text += "font color<br>"
        edit_box_text += "selected node color<br>"
        edit_box_text += "selected edge color<br>"
        edit_box_text += "searched node color<br>"
        edit_box_text += "By clicking the set colors button, you can change the appearance of the graph.<br>"
        edit_box_text += f'<img src = {absolute_path + "/edit_box.jpg"}><br>'

        node_attributes_text = "<b>Node attributes</b><br> You can view the attributes of a node by selecting it.<br>"
        node_attributes_text += "The attributes will be shown in a popup when you click the show information button.<br>"
        node_attributes_text += f'<img src = {absolute_path + "/show_info_button.jpg"}><br>'
        node_attributes_text += "There, you will find the connections of the node by sub id and name.<br>"
        node_attributes_text += f'<img src = {absolute_path + "/node_attributes.jpg"}><br>'
        node_attributes_text += "You can also view attributes of edges by selecting an edge.<br>"

        interacting_text = "<b>Interacting with the graph</b><br> You can move the graph by clicking and dragging on the background.<br>"
        interacting_text += "You can zoom in and out by scrolling with the mouse wheel.<br>"
        interacting_text += f'<img src = {absolute_path + "/zoom.jpg"}><br>'
        interacting_text += f'<img src = {absolute_path + "/zoom_out.jpg"}><br>'
        interacting_text += "You can resize the window anytime you want.<br>"
        interacting_text += "You can move a single node by clicking and dragging it.<br>"

        self.menu_points = {
            'Welcome': '<b>Welcome to the help menu!</b><br> Here you can find all the information you need to use the application.',
            'Load a graph': load_a_graph_text,
            'Save a graph': save_a_graph_text,
            'Select a node': select_a_node_text,
            'Focus on a node': focus_on_a_node_text,
            'Search box': search_box_text,
            'Edit box': edit_box_text,
            'Node attributes': node_attributes_text,
            'Interacting with the graph': interacting_text
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

        # Create a right panel inside the popup for the Help menu.
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

        # Create a text box inside the right panel for the Help menu.
        self.text_box = pgui.elements.UITextBox(
            relative_rect=pg.Rect(0, 0, 600, 800),
            html_text=self.menu_points['Welcome'],
            manager=self.manager,
            container=right_panel
        )

        self.popup.set_blocking(True)

    # Handle the event of a menu button being pressed.
    def handle_menu_button_pressed(self, button):
        # Get the text of the button that was pressed.
        text = button.text

        # Get the corresponding text from the menu_points dictionary.
        menu_text = self.menu_points[text]

        # Set the text of the text box in the right panel.
        self.text_box.set_text(menu_text)

    # Handle the event of the Load button being pressed.
    def handle_load_button_pressed(self, column_names):
        # Define the columns that must be present in the loaded file.
        must_have_columns = ['node_id', 'sub_id', 'connections']
        optional_columns = ['node_name', 'sub_id_value_name']

        # Initialize the load popup window.
        self.load_popup = pgui.elements.UIWindow(
            rect=pg.Rect(0, 0, 450, 500),
            manager=self.manager,
            window_display_title='Load a Graph'
        )

        # Create a panel inside the popup window.
        panel = pgui.elements.UIPanel(
            relative_rect=pg.Rect(0, 0, 450, 500),
            starting_height=0,
            manager=self.manager,
            container=self.load_popup,
            anchors={
                'left': 'left',
                'right': 'right',
                'top': 'top',
                'bottom': 'bottom'
            }
        )

        # Add description text area.
        description_text_area = pgui.elements.UITextBox(
            relative_rect=pg.Rect(10, 10, 430, 80),
            html_text='<b>Please pair the row names.</b><br>Every row that\'s not paired will be in the "other" category.',
            manager=self.manager,
            container=panel
        )

        # Create a list of items to populate the dropdowns.
        items = ['None']
        for column in column_names:
            items.append(column)

        y_position = 100
        must_have_dropdowns = []

        # Create dropdowns for must-have columns.
        for i, column_name in enumerate(must_have_columns):
            label = pgui.elements.UILabel(
                relative_rect=pg.Rect(10, y_position + i * 40, 200, 30),
                text=column_name,
                manager=self.manager,
                container=panel
            )

            dropdown = pgui.elements.UIDropDownMenu(
                relative_rect=pg.Rect(220, y_position + i * 40, 200, 30),
                options_list=items,
                starting_option=items[0],
                manager=self.manager,
                container=panel
            )
            must_have_dropdowns.append(dropdown)
            last_pos = y_position + i * 40

        optional_dropdowns = []

        size = len(must_have_columns)

        # Create dropdowns for optional columns.
        for i, column_name in enumerate(optional_columns):
            label = pgui.elements.UILabel(
                relative_rect=pg.Rect(10, y_position + (i + size) * 40, 200, 30),
                text=column_name + ' (optional)',
                manager=self.manager,
                container=panel
            )

            dropdown = pgui.elements.UIDropDownMenu(
                relative_rect=pg.Rect(220, y_position + (i + size) * 40, 200, 30),
                options_list=items,
                starting_option=items[0],
                manager=self.manager,
                container=panel
            )
            optional_dropdowns.append(dropdown)
            last_pos = last_pos + 40 + i * 40

        # Add Okay button.
        okay_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(10, last_pos + 40, 200, 50),
            text='Okay',
            manager=self.manager,
            container=panel
        )
        okay_button.disable()

        # Add Cancel button.
        cancel_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(220, last_pos + 40, 200, 50),
            text='Cancel',
            manager=self.manager,
            container=panel
        )

        status_label = pgui.elements.UILabel(
            relative_rect=pg.Rect(10, last_pos + 100, 430, 30),
            text='Please don\'t leave any required columns empty.',
            manager=self.manager,
            container=panel
        )

        # Store the popup items.
        self.load_popup_items = {
            'must_have': must_have_dropdowns,
            'optional': optional_dropdowns,
            'okay_button': okay_button,
            'cancel_button': cancel_button,
            'status_label': status_label
        }
        self.load_popup.set_blocking(True)

    # Handle the event of a must-have dropdown being changed.
    def handle_must_have_dropdown_changed(self):
        for dropdown in self.load_popup_items['must_have']:
            if dropdown.selected_option[0] == 'None':
                self.load_popup_items['okay_button'].disable()
                self.load_popup_items['status_label'].set_text('Please don\'t leave any required columns empty.')
                return
        all_dropdowns = self.load_popup_items['must_have'] + self.load_popup_items['optional']
        for dropdown_1 in all_dropdowns:
            for dropdown_2 in all_dropdowns:
                if dropdown_1 != dropdown_2 and dropdown_1.selected_option == dropdown_2.selected_option and dropdown_1.selected_option[0] != 'None':
                    self.load_popup_items['okay_button'].disable()
                    self.load_popup_items['status_label'].set_text('Please don\'t pair the same column twice.')
                    return
        self.load_popup_items['okay_button'].enable()
        self.load_popup_items['status_label'].set_text('')

    # Handle the event of the Okay button being pressed in the load popup.
    def handle_load_popup_okay_button_pressed(self):
        must_have_columns = ['node_id', 'sub_id', 'connections']
        optional_columns = ['node_name', 'sub_id_value_name']

        must_have_pairings = {
            'node_id': 'None',
            'sub_id': 'None',
            'connections': 'None'
        }

        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'None'
        }

        for i, dropdown in enumerate(self.load_popup_items['must_have']):
            must_have_pairings[must_have_columns[i]] = dropdown.selected_option[0]

        for i, dropdown in enumerate(self.load_popup_items['optional']):
            optional_pairings[optional_columns[i]] = dropdown.selected_option[0]

        self.load_popup.kill()
        return must_have_pairings, optional_pairings

    # Resize the UIHeader to the given width and height.
    def resize(self, width, height, window, manager):
        self.window = window
        self.manager = manager
        self.width = width
        self.height = height

        # Hide and kill old elements
        self.killall()
        self.base_panel = self.create_base_panel()
        self.create_buttons()

    # Handle the event of the Cancel button being pressed in the load popup.
    def handle_load_popup_cancel_button_pressed(self):
        self.load_popup.kill()

    # Kill all the elements in the UIHeader.
    def killall(self):
        self.load_button.kill()
        self.save_button.kill()
        self.help_button.kill()
        self.base_panel.kill()

    # Process the given event.
    def process_events(self, event):
        self.manager.process_events(event)

    def draw_ui(self):
        self.manager.draw_ui(self.window)

    def get_manager(self):
        return self.manager

    def update(self, time_delta):
        self.manager.update(time_delta)
