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
            sleep(0.1)
            gpio.output(self.pin_number,gpio.HIGH)
            sleep(0.3)

    def ringerror(self):
        for i in range(6):
            gpio.output(self.pin_number,gpio.LOW)
            sleep(0.6)
            gpio.output(self.pin_number,gpio.HIGH)
            sleep(0.1)

    def positiveresponse(self):
        gpio.output(self.pin_number,gpio.LOW)
        sleep(0.1)
        gpio.output(self.pin_number,gpio.HIGH)
        sleep(0.1)
        gpio.output(self.pin_number,gpio.LOW)
        sleep(0.1)
        gpio.output(self.pin_number,gpio.HIGH)


    def __del__(self):
        gpio.cleanup(self.pin_number)
