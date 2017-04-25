#!/usr/bin/env python
import os
import time
import colorsys
import threading
import rainbowhat

# Touch events
@rainbowhat.touch.press()
def touch_press(channel):
    global inputs
    # Reset all states to false
    inputs = [False, False, False]
    rainbowhat.lights.rgb(0, 0, 0)
    # Set the selected button status to true and turn on LED
    inputs[channel] = True
    rainbowhat.lights[channel].on()

class DisplayThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        set_display()

class RainbowThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        set_rainbow()

def get_ambient_temperature():
    # Getting CPU temperature from Raspberry Pi
    res = os.popen('vcgencmd measure_temp').readline()
    cpu_temp = int(float((res.replace("temp=","").replace("'C\n",""))))
    # Getting temperature from RainbowHat thermometer
    rainbowhat_temp = rainbowhat.weather.temperature()
    # Calculate estimated temperature
    return rainbowhat_temp - (cpu_temp - rainbowhat_temp) / 2

def set_display():
    while True:
        rainbowhat.display.clear()

        if inputs[A]:
            temperature = get_ambient_temperature()
            rainbowhat.display.print_float(temperature)

        if inputs[B]:
            pressure = rainbowhat.weather.pressure()/100
            rainbowhat.display.print_float(pressure)

        if inputs[C]:
            current_time = time.strftime("%H%M")
            rainbowhat.display.print_str(current_time)

        rainbowhat.display.show()
        time.sleep(0.1)

def set_rainbow():
    while True:
        for x in range(7):
            delta = time.time() * 20
            hue = delta + (x*10)
            hue %= 360
            hue /= 360.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
            rainbowhat.rainbow.set_pixel(6-x, r, g, b, brightness=0.1)
        rainbowhat.rainbow.show()
        time.sleep(0.05)

# Clear existing display
rainbowhat.display.clear()
rainbowhat.display.show()

# Buttons identifier
A = 0
B = 1
C = 2

# Setting up initial state
inputs = [True, False, False]
rainbowhat.lights[A].on()

# Create new threads
display_thread = DisplayThread()
rainbow_thread = RainbowThread()

# Start new Threads
display_thread.start()
rainbow_thread.start()
