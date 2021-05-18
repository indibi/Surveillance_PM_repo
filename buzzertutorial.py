#Libraries
#https://peppe8o.com/use-passive-buzzer-with-raspberry-pi-and-python/
import RPi.GPIO as gpio
from time import sleep


class Buzzer(object):
    def __init(self,pin_number):
        gpio.setmode(gpio.BOARD)
        self.buzzer = GPIO.PWM(self.pin_number, 3000) # Set frequency to 1 Khz

    def ringwarning(self):
        self.buzzer.start(40) # Set dutycycle to 10

    def ringerror(self):
        self.buzzer.start(70) # Set dutycycle to 50

    def stop(self):
        self.buzzer.stop()
