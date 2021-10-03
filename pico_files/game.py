from machine import Pin, SPI, ADC
from utime import sleep_ms, ticks_ms
from st7789 import LCD
from graphics import Graphics

import math
import sys

"""
TODO:
- Multithreading for inputs, learning about stabilizing pots
- Rewrite modules in c
"""

class Cons:
    WIDTH = 320
    HEIGHT = 240
    TIMESTEP = 30

    BL = 13
    DC = 8
    RST = 12
    DIN = 11
    CLK = 10
    CS = 9

    WHITE  = 0xFFFF
    BLACK  = 0x0000
    GREEN  = 0x001F
    RED    = 0xF800
    BLUE   = 0x07E0
    GBLUE  = 0X07FF
    YELLOW = 0xFFE0
    ORANGE = 0xFBE0
    CYAN   = 0x7FF
    PINK   = 0xF81F
    PURPLE = 0xD01F

    FUN_COLS = [GREEN, RED, BLUE, GBLUE, YELLOW, ORANGE, CYAN, PINK, PURPLE]

class GameObject():
    def __init__(self):
        self.remove = False

    def update(self):
        """ Updates the Object """

    def draw(self, graphics):
        """ Draws the Game """

class Game():
    def __init__(self):
        # SCREEN
        self.spi = SPI(1, 412500000, polarity=0, phase=0, sck=Pin(Cons.CLK), mosi=Pin(Cons.DIN), miso=None)
        self.lcd = LCD(self.spi, Cons.WIDTH, Cons.HEIGHT, Cons.CS, Cons.RST, Cons.BL, Cons.DC)

        # GRAPHICS
        self.gfx = Graphics(
            width  = Cons.WIDTH,
            height = Cons.HEIGHT,
            pixel  = self.lcd.pixel,
            hline  = self.lcd.hline,
            vline  = self.lcd.vline,
            text   = self.lcd.text)

        # CONTROLS
        self.pot1 = ADC(26)
        self.pot2 = ADC(28)
        self.scaled = 65535 / 365
        self.left_stick  = 0
        self.right_stick = 0

        # OBJECTS
        self.game_objects: list[GameObject] = []

        # TIMING
        self.timer = ticks_ms()
        self.tickrate = int(1000 / Cons.TIMESTEP)
        self.fps = 0

        # BACKLIGHT
        Pin(Cons.BL).value(1)

    def add_object(self, obj: GameObject):
        self.game_objects.append(obj)

    def remove_object(self, obj: GameObject):
        self.game_objects.remove(obj)


    def run(self):
        self.running = True
        self._run()

    def _run(self):
        while self.running:
            dt = 0
            t = ticks_ms()

            self.update()
            self.draw()

            dt = ticks_ms() - t
            self.fps = int(1000/dt)
            if dt < self.tickrate:
                sleep_time = (self.tickrate - dt)
                sleep_ms(sleep_time)

    def update(self):
        """Updates the game."""
        self.left_stick  = self.pot1.read_u16()/self.scaled
        self.right_stick = self.pot2.read_u16()/self.scaled

        for obj in self.game_objects:
            obj.update()
            if obj.remove:
                self.remove_object(obj)

    def draw(self):
        self.lcd.fill(0x000)
        """Draws the game."""
        for obj in reversed(self.game_objects):
            obj.draw(self.gfx)
        self.lcd.show()


def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
