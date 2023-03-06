from iotutils_neopixel import Neopixel
from colorzero import Color, Hue
import time

ledCount = 10
ledPin = 18

neop = Neopixel(ledCount, ledPin)
color = Color("white")

while True:
    try:
        for i in range(50):
            neop.fill(color)
            neop.changeBrightness(i/100)
            neop.show()
            time.sleep(0.06)

        for ledId in reversed(range(ledCount)):
            time.sleep(0.02)
            neop.setColor(ledId, Color("black"))
            neop.show()
        time.sleep(1)
    except KeyboardInterrupt:
        break
    
neop.fill(Color("black"))
neop.show()




