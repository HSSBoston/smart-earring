# Library to use a Neopixel stick/strip/ring
# Feb 23, 2023 v0.04
# IoT for Kids: https://jxsboston.github.io/IoT-Kids/
#
# Neopixel implemented as a subclass of rpi_ws281x.PixelStrip.
# See https://github.com/rpi-ws281x/rpi-ws281x-python for the
# Python binding of rpi_ws281x. 

import rpi_ws281x, colorzero, math

class Neopixel(rpi_ws281x.PixelStrip):
    def __init__(self, ledCount, signalPin, freq_hz=800000, dma=10, invert=False,
                 brightness=63, channel=0, strip_type=None, gamma=None):
        super().__init__(ledCount, signalPin, freq_hz, dma, invert, brightness,
                         channel, strip_type, gamma)
        self.begin()
    
    # Change the brightness of LEDs.
    # brightness (float): [0.0, 1.0], Default: 0.25
    #
    def changeBrightness(self, brightness):
        self.setBrightness(math.floor(brightness * 255))
    
    # Set a colorzero.Color to a particular LED
    #   ledPosition (int): LED's position (ID), [0, ledCount-1]
    #   colorzeroColor (colorzero.Color): Color to be set a particular LED
    #
    def setColor(self, ledPosition, colorzeroColor, white=0):
        red = colorzeroColor.rgb_bytes[0]
        green = colorzeroColor.rgb_bytes[1]
        blue = colorzeroColor.rgb_bytes[2]
        self.setPixelColor(ledPosition, rpi_ws281x.Color(red, green, blue, white))

    # Set a tuple of R, G and B values to a particular LED
    #   ledPosition (int): LED's position (ID), [0, ledCount-1]
    #   colorTuple: Tuple of R, G, B values. Each RGB value is [0,256].
    #
    def setRGB(self, ledPosition, colorTuple, white=0):
        red = colorTuple[0]
        green = colorTuple[1]
        blue = colorTuple[2]
        self.setPixelColor(ledPosition, rpi_ws281x.Color(red, green, blue, white))

#     def setRGB(self, ledPosition, red, green, blue, white=0):
#         self.setPixelColor(ledPosition, rpi_ws281x.Color(red, green, blue, white))
    
    # Set a single color to all LEDs
    #   colorzeroColor (colorzero.Color): Color to be set to all LEDs
    #
    def fill(self, colorzeroColor, white=0):
        red = colorzeroColor.rgb_bytes[0]
        green = colorzeroColor.rgb_bytes[1]
        blue = colorzeroColor.rgb_bytes[2]
        self.fillRGB((red, green, blue), white)

    # Set a single color to all LEDs
    #   colorTuple: Tuple of R, G, B values. Each RGB value is [0,256].
    #
    def fillRGB(self, colorTuple, white=0):
        for ledPos in range(self.numPixels()):
            self.setPixelColor(ledPos, rpi_ws281x.Color(colorTuple[0],
                                                        colorTuple[1],
                                                        colorTuple[2],
                                                        white))

    # Return a colorzero.Color for a particular LED.
    #   ledPosition (int): LED's position (ID), [0, ledCount-1]
    #
    def getColor(self, ledPosition):
        rgbTuple = self.getRGB(ledPosition)
        return colorzero.Color(rgbTuple[0], rgbTuple[1], rgbTuple[2])

    # Return a tuple of R, G and B values for a particular LED.
    # Each RGB value is [0,256].
    #   ledPosition (int): LED's position (ID), [0, ledCount-1]
    #
    def getRGB(self, ledPosition):
        rgbwTuple = self.getRGBW(ledPosition)
        return (rgbwTuple[0], rgbwTuple[1], rgbwTuple[2])

    # Return a tuple of R, G, B and W values for a particular LED.
    # Each RGBW value is [0,256].
    #   ledPosition (int): LED's position (ID), [0, ledCount-1]
    #    
    def getRGBW(self, ledPosition):
        color = self.getPixelColor(ledPosition)
        white = color >> 24 & 0xff
        red = color >> 16 & 0xff
        green = color >> 8  & 0xff
        blue = color & 0xff
        return (red, green, blue, white)    

