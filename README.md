# Smart Earring: Sound-Sensitive and Siri-ready LED Bar for Earrings

This is a a sound-sensitive LED bar for earrings. Its 10 RGB LEDs are controlled by a Raspberry Pi Zero. It "hears” (records) ambient sound and emits lights according to its volume. It emits more lights with red and other loud colors for louder sound. It emits less lights with green and other soft colors for quiet sound. This device is Siri-ready; it runs with a voice command.

<img src="images/earring.jpg" width=250><img src="images/earring2.jpg" width=250>

## Equipment
- Raspberry Pi Zero
- Seeed Studio’s Grove LED bar
- Microphone (USB, wired)
- Earring hook

## Hardware Setup

- Connected an LED bar to Raspi
- Connected a microphone to Raspi
- Put an earring hook to the LED bar.

## Software Setup

- Wrote a Python program that 
  - Records ambient sound every 0.1 second with the “pyaudio” module,
  - Finds the highest amplitude (volume level) in the recorded sound wave, and 
  - Emits different lights with different lights according to its volume. 
- Wrote a Python program that flushes LEDs in white before recording ambient sound. 
- Made a Shortcut app on iPad to run Python code.

## Demo

<img src="images/earring3.jpg" width="500">

https://user-images.githubusercontent.com/74394277/223153115-51956d59-aaff-4509-8b5a-2b0eea5d7f91.mp4

https://user-images.githubusercontent.com/74394277/223153477-637d6a36-607b-41d4-b50d-b0a78eb55331.mp4

https://user-images.githubusercontent.com/74394277/223153730-633deb89-b5ff-490f-bf19-26bed7aac50a.mp4

