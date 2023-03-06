from iotutils_neopixel import Neopixel
from colorzero import Color, Hue
import time

ledCount = 10
ledPin = 18
degreeAdjustment = 360/ledCount

neop = Neopixel(ledCount, ledPin)

firstColor = Color("red")

for ledId in range(ledCount):
    degree = ledId * degreeAdjustment
    neop.setColor(ledId, firstColor + Hue(deg=degree))
    neop.show()
    time.sleep(0.1 - 0.009 * ledId)

for ledId in reversed(range(ledCount)):
    time.sleep(0.02)
    neop.setColor(ledId, Color("black"))
    neop.show()




