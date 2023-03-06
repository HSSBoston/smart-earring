from iotutils_neopixel import Neopixel
from colorzero import Color, Hue
import time

ledCount = 10
ledPin = 18
degreeAdjustment = 360/ledCount

neop = Neopixel(ledCount, ledPin)
firstLedColor = Color("red")

for ledId in range(ledCount):
    degree = ledId * degreeAdjustment
    neop.setColor(ledId, firstLedColor + Hue(deg=degree))
neop.show()
time.sleep(5)

neop.fill(Color("black"))
neop.show()



