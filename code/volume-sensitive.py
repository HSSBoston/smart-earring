import soundin, time, sound_analysis as sa
from iotutils_neopixel import Neopixel
from colorzero import Color, Hue

ledCount = 10
ledPin = 18
volThreshold = 0.1
ledOnDuration = 0.02

stream = soundin.init()
neop = Neopixel(ledCount, ledPin)
prevOnLedCount = 0

ledColors = [Color("yellow")]
degreeAdjustment = 330/ledCount
for ledId in range(1, ledCount):
    nextColor = ledColors[ledId-1] - Hue(deg=degreeAdjustment)
    ledColors.append(nextColor)

while True:
    try:
        soundSamples = soundin.capture(stream)
        maxVolLevel = max(soundSamples)

        if maxVolLevel < volThreshold:
            print(".....")
        else:
            print("Volume: " + str(maxVolLevel))
        
        onLedCount = int(round((maxVolLevel * ledCount), 0))
        if onLedCount < prevOnLedCount:
            neop.fill(Color("black"))
            neop.show()            
        for led in range(onLedCount):
            neop.setColor((ledCount-1)-led, ledColors[(ledCount-1)-led])
            neop.show()
        prevOnLedCount = onLedCount
        time.sleep(ledOnDuration)
            
    except KeyboardInterrupt:
        break

neop.fill(Color("black"))
neop.show()
soundin.close(stream)