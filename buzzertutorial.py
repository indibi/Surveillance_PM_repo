#Libraries
#https://peppe8o.com/use-passive-buzzer-with-raspberry-pi-and-python/
import RPi.GPIO as gpio
from time import sleep


class Buzzer(object):
    def __init__(self,pin_number):
        gpio.setmode(gpio.BOARD)
        self.pin_number=pin_number
        gpio.setup(pin_number, gpio.OUT, initial=gpio.HIGH)

    def ringwarning(self):
        for i in range(3):
            gpio.output(self.pin_number,gpio.LOW)
            sleep(0.2)
            gpio.output(self.pin_number,gpio.HIGH)
            sleep(0.3)

    def ringerror(self):
        for i in range(4):
            gpio.output(self.pin_number,gpio.LOW)
            sleep(0.5)
            gpio.output(self.pin_number,gpio.HIGH)
            sleep(0.15)

    def positiveresponse(self):
        for i in range(2):
            gpio.output(self.pin_number,gpio.LOW)
            sleep(0.2)
            gpio.output(self.pin_number,gpio.HIGH)
            sleep(0.3)

    def __del__(self):
        gpio.cleanup(self.pin_number)




buzzer = Buzzer(33)

buzzer.ringwarning()
buzzer.ringerror()
buzzer.positiveresponse()
