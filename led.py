import RPi.GPIO as gpio
import time



class led(object):
    def __init__(self,led_pin):
        self.led_pin = led_pin
        gpio.setup(self.led_pin, gpio.OUT)
        gpio.output(self.led_pin,0)

    def light(self):
        gpio.output(self.led_pin,1)

    def putout(self):
        gpio.output(self.led_pin,0)

    def __del__(self):
        gpio.cleanup(gpio.led_pin)
