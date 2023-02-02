# PiPicoWHomekitDoorLock

Unlock the front door using a Raspberry Pi Pico W and Homebridge.


# YouTube Video
To learn more, check out the YouTube video I made about the Garage Door Opener

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/tJPmqTGcAxA/0.jpg)](https://www.youtube.com/watch?v=tJPmqTGcAxA)

# Setting up the hardware
In order to control the door and detect if the door is opened or closed, we just need to use a single pin on the Raspberry Pi Pico.

The pin that I have chosen is pin 16.

The relay connects directly between Pin 16 and ground.

# Installation on the Pi Pico

Make sure that you have Micropython installed on your Raspberry Pi Pico.

Edit the wifi setting in the config.py file and upload the config.py and main.py file through your favourite tool, such as Thonny.

# Connecting to Homebridge

In order to connect the Pi Pico to Homebridge, I'm using the HTTP Advanced Accessory plugin by staromeste.

You can find the plugin here: https://github.com/staromeste/homebridge-http-advanced-accessory

This plugin is very powerful, but not very user friendly as it needs to be configured using JSON to talk to and understand accessories.

But don't despair. I included a working configuration file in this repository. Just copy and paste the contents into the plugin configuration. The only thing you need to do is replace "YOUR_PI_PICO" with the IP-address of your device.
