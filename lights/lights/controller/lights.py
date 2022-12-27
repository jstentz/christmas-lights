import neopixel
import random
import colorsys

class Lights(neopixel.NeoPixel):
    def clear(self):
        self.fill((0, 0, 0))

    def update(self, newPixels):
        for i in range(len(newPixels)):
            self[i] = newPixels[i]

    @staticmethod
    def randomColor():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    @staticmethod
    def hsv_to_rgb(h, s, v):
        return (int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v))
