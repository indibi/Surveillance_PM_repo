#Libraries
#https://peppe8o.com/use-passive-buzzer-with-raspberry-pi-and-python/
import RPi.GPIO as gpio
from time import sleep


class Buzzer(object):
    def __init(self,pin_number):
        gpio.setmode(gpio.BOARD)
        buzzer = GPIO.PWM(self.pin_number, 1000) # Set frequency to 1 Khz

    def ringwarning():
        buzzer.start(10) # Set dutycycle to 10

    def ringerror():
        buzzer.start(50) # Set dutycycle to 50
        
    def stop():
        buzzer.stop()
