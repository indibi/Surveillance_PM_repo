import RPi.GPIO as gpio
import time



class led(object):
    def __init(self,led_pin):
        gpio.setup(self.led_pin, gpio.OUT)


    def light():
        gpio.output(self.led_pin,1)

    def putout():
        gpio.output(self.led_pin,0)
