import pygame as pg

from src.view.arrow import Arrow
import unittest
from unittest.mock import patch, mock_open, MagicMock, call, PropertyMock


class TestArrow(unittest.TestCase):
    def test_init(self):
        window = MagicMock()
        button_start = MagicMock()
        button_end = MagicMock()
        arrow = Arrow(window, button_start, button_end)
        self.assertEqual(arrow.window, window)
        self.assertEqual(arrow.button_start, button_start)
        self.assertEqual(arrow.button_end, button_end)
        self.assertEqual(arrow.color, (136, 136, 136))
        self.assertEqual(arrow.size, 2)
        self.assertEqual(arrow.arrowhead_size, 10)
        self.assertEqual(arrow.unzoomed_size, 2)
        self.assertEqual(arrow.unzoomed_arrowhead_size, 10)

    @patch('src.view.arrow.pg.draw.line')
    def test_draw(self, mock_pg_draw_line):
        window = MagicMock()
        button_start = MagicMock()
        button_start.x = 1
        button_start.y = 2
        button_end = MagicMock()
        button_end.x = 3
        button_end.y = 4
        arrow = Arrow(window, button_start, button_end)
        arrow.draw()
        mock_pg_draw_line.assert_called_once_with(arrow.window, arrow.color, (1, 2), (3, 4), arrow.size)

    def test_zoom(self):
        window = MagicMock()
        button_start = MagicMock()
        button_end = MagicMock()
        arrow = Arrow(window, button_start, button_end)
        zoom_scale = 2
        with patch.object(arrow, 'draw') as mock_draw:
            arrow.zoom(zoom_scale)
            mock_draw.assert_called_once()

        self.assertEqual(arrow.size, int(arrow.unzoomed_size * zoom_scale))
        self.assertEqual(arrow.arrowhead_size, int(arrow.unzoomed_arrowhead_size * zoom_scale))

    def test_change_color(self):
        window = MagicMock()
        button_start = MagicMock()
        button_end = MagicMock()
        arrow = Arrow(window, button_start, button_end)
        color = (255, 255, 255)
        with patch.object(arrow, 'draw') as mock_draw:
            arrow.change_color(color)
            mock_draw.assert_called_once()

        self.assertEqual(arrow.color, color)

    def test_handle_click(self):
        window = MagicMock()
        button_start = MagicMock()
        button_start.x = 1
        button_start.y = 2
        button_end = MagicMock()
        button_end.x = 3
        button_end.y = 4
        arrow = Arrow(window, button_start, button_end)
        event = MagicMock()
        event.type = pg.MOUSEBUTTONDOWN
        event.pos = (2, 3)
        with patch('src.view.arrow.abs') as mock_abs, \
             patch('src.view.arrow.pg.draw.line') as mock_pg_draw_line:
            mock_abs.return_value = 20
            self.assertEqual(arrow.handle_click(event), 0)

    def test_handle_click_small_distance(self):
        window = MagicMock()
        button_start = MagicMock()
        button_start.x = 1
        button_start.y = 2
        button_end = MagicMock()
        button_end.x = 3
        button_end.y = 4
        arrow = Arrow(window, button_start, button_end)
        event = MagicMock()
        event.type = pg.MOUSEBUTTONDOWN
        event.pos = (2, 3)
        with patch('src.view.arrow.abs') as mock_abs, \
                patch('src.view.arrow.pg.draw.line') as mock_pg_draw_line:
            mock_abs.return_value = 5
            self.assertEqual(arrow.handle_click(event), 1)

    def test_handle_click_not_good_event(self):
        window = MagicMock()
        button_start = MagicMock()
        button_start.x = 1
        button_start.y = 2
        button_end = MagicMock()
        button_end.x = 3
        button_end.y = 4
        arrow = Arrow(window, button_start, button_end)
        event = MagicMock()
        event.type = pg.MOUSEMOTION
        event.pos = (2, 3)
        with patch('src.view.arrow.abs') as mock_abs, \
                patch('src.view.arrow.pg.draw.line') as mock_pg_draw_line:
            mock_abs.return_value = 20
            self.assertEqual(arrow.handle_click(event), 0)
