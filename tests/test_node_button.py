import unittest
from unittest.mock import patch, MagicMock
import pygame as pg

from src.view.node_button import NodeButton


class TestNodeButton(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.font.init()

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    @patch('src.view.node_button.pg.font.Font', return_value=MagicMock())
    @patch.object(NodeButton, 'calculate_font_size', return_value=12)
    def test_init(self, mock_calculate_font_size, mock_font):
        # Arrange
        surface = MagicMock()
        node = MagicMock()
        node.id = 1

        # Act
        button = NodeButton(surface, 1, 2, 3, node)

        # Assert
        self.assertEqual(button.surface, surface)
        self.assertEqual(button.x, 1)
        self.assertEqual(button.y, 2)
        self.assertEqual(button.radius, 3)
        self.assertEqual(button.color, (0, 92, 37))
        self.assertEqual(button.node, node)
        self.assertEqual(button.text, 1)
        self.assertEqual(button.text_color, (255, 255, 255))
        self.assertEqual(button.font_size, 12)
        self.assertEqual(button.font, mock_font.return_value)
        self.assertEqual(button.last_click_time, 0)
        self.assertEqual(button.last_click_pos, (0, 0))
        self.assertEqual(button.unscaled_font_size, 12)
        self.assertEqual(button.unscaled_radius, 3)

        mock_font.assert_called_once_with(None, 12)
        mock_calculate_font_size.assert_called_once()

    @patch('src.view.node_button.pg.draw.circle')
    @patch.object(NodeButton, 'get_font', return_value=MagicMock())
    def test_draw(self, mock_get_font, mock_draw_circle):
        # Arrange
        surface = MagicMock()
        node = MagicMock()
        node.id = "test"
        button = NodeButton(surface, 1, 2, 15, node)

        # Act
        with patch.object(button, 'font', return_value=MagicMock()) as mock_font:
            button.draw()

        button.draw()

    @patch.object(NodeButton, 'draw')
    def test_set_position(self, mock_draw):
        # Arrange
        surface = MagicMock()
        node = MagicMock()
        node.id = "test"
        button = NodeButton(surface, 1, 2, 3, node)

        # Act
        button.set_position(10, 20)

        # Assert
        self.assertEqual(button.x, 10)
        self.assertEqual(button.y, 20)
        mock_draw.assert_called_once()

    @patch.object(NodeButton, 'draw')
    def test_move(self, mock_draw):
        # Arrange
        surface = MagicMock()
        node = MagicMock()
        node.id = "test"
        button = NodeButton(surface, 1, 2, 3, node)

        # Act
        button.move(5, 5)

        # Assert
        self.assertEqual(button.x, 6)
        self.assertEqual(button.y, 7)
        mock_draw.assert_called_once()

    @patch.object(NodeButton, 'draw')
    @patch.object(NodeButton, 'get_font', return_value=MagicMock())
    def test_zoom(self, mock_get_font, mock_draw):
        # Arrange
        surface = MagicMock()
        node = MagicMock()
        node.id = "test"
        button = NodeButton(surface, 10, 10, 10, node)
        zoom_center = (5, 5)

        # Act
        button.zoom(2, 1.5, zoom_center)

        # Assert
        self.assertEqual(button.radius, 15)
        self.assertEqual(button.x, 12)
        self.assertEqual(button.y, 12)
        self.assertEqual(button.font_size, 13)
        mock_get_font.assert_called_once_with(13)
        mock_draw.assert_called_once()

    @patch.object(NodeButton, 'draw')
    def test_change_colors(self, mock_draw):
        # Arrange
        surface = MagicMock()
        node = MagicMock()
        node.id = "test"
        button = NodeButton(surface, 1, 2, 3, node)
        colors = {
            'selected_node': (255, 0, 0),
            'searched_node': (0, 255, 0),
            'node': (0, 0, 255),
            'text': (255, 255, 255)
        }

        # Act
        button.change_colors(colors, selected=True)
        self.assertEqual(button.color, (255, 0, 0))

        button.change_colors(colors, searched=True)
        self.assertEqual(button.color, (0, 255, 0))

        button.change_colors(colors)
        self.assertEqual(button.color, (0, 0, 255))
        self.assertEqual(button.text_color, (255, 255, 255))
        mock_draw.assert_called()

    def test_information_dict(self):
        # Arrange
        surface = MagicMock()
        node = MagicMock()
        node.id = "test"
        node.attributes = {'key': 'value'}
        button = NodeButton(surface, 1, 2, 3, node)

        # Act
        info = button.information_dict()

        # Assert
        self.assertEqual(info, {'key': 'value'})

    def test_handle_click(self):
        # Arrange
        event = MagicMock()
        event.type = pg.MOUSEBUTTONDOWN
        event.pos = (1, 2)
        time = 0.3
        button = NodeButton(MagicMock(), 1, 2, 3, MagicMock())

        # Act
        result = button.handle_click(event, time)

        # Assert
        self.assertEqual(result, 1)
        self.assertEqual(button.last_click_time, time)
        self.assertEqual(button.last_click_pos, event.pos)


if __name__ == '__main__':
    unittest.main()
