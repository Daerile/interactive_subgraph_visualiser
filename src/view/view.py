import pygame as pg
import sys


class View:
    def __init__(self):
        pg.init()
        self.WIDTH = 1920
        self.HEIGHT = 1080
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.start_up()

    def start_up(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            self.window.fill((255,255,255))
            pg.display.update()
        pg.quit()
        sys.exit()