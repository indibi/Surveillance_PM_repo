import RPi.GPIO as gpio
from time import sleep
import threading

class Buzzer(object):
    def __init__(self,pin_number):
        gpio.setmode(gpio.BOARD)
        self.pin_number=pin_number
        gpio.setup(pin_number, gpio.OUT, initial=gpio.HIGH)

        self.door_thread = threading.Thread(target= self._thread_loop)
        self._order_list = 0
        self._order_lock = threading.Lock()
        self.door_thread.start()

    def positiveresponse(self):
        self._order_lock.acquire()
        if self._order_list ==0:
            self._order_list = 1
            self._order_lock.release()
            return 1
        else:
            self._order_lock.release()
            return 0

    def ringwarning(self):
        self._order_lock.acquire()
        if self._order_list ==0:
            self._order_list = 2
            self._order_lock.release()
            return 2
        else:
            self._order_lock.release()
            return 0

    def ringerror(self):
        self._order_lock.acquire()
        if self._order_list ==0:
            self._order_list = 3
            self._order_lock.release()
            return 3
        else:
            self._order_lock.release()
            return 0

    def _thread_loop(self):
        while True:
            self._order_lock.acquire()
            a = self._order_list
            self._order_list=0
            self._order_lock.release()
            if a== 1:
                self._positiveresponse()
            elif a == 2:
                self._ringwarning()
            elif a == 3:
                self._ringerror()
            else:
                sleep(0.4)

    def _ringwarning(self):
        for i in range(3):
            gpio.output(self.pin_number,gpio.LOW)
            sleep(0.1)
            gpio.output(self.pin_number,gpio.HIGH)
            sleep(0.3)

    def _ringerror(self):
        for i in range(6):
            gpio.output(self.pin_number,gpio.LOW)
            sleep(0.6)
            gpio.output(self.pin_number,gpio.HIGH)
            sleep(0.1)

    def _positiveresponse(self):
        gpio.output(self.pin_number,gpio.LOW)
        sleep(0.1)
        gpio.output(self.pin_number,gpio.HIGH)
        sleep(0.1)
        gpio.output(self.pin_number,gpio.LOW)
        sleep(0.1)
        gpio.output(self.pin_number,gpio.HIGH)


    def __del__(self):
        gpio.output(self.pin_number,gpio.HIGH)
        gpio.cleanup(self.pin_number)
