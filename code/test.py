from iotutils_neopixel import Neopixel
from colorzero import Color, Hue
import time

ledCount = 10
ledPin = 18

neop = Neopixel(ledCount, ledPin)

neop.setColor(0, Color("yellow"))
neop.show()
time.sleep(2)

neop.fill(Color("black"))
neop.show()

neop.fill(Color("red"))
neop.changeBrightness(0.25)
neop.show()
time.sleep(2)

neop.fill(Color("black"))
neop.show()
