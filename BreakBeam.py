import RPi.GPIO as gpio
import time, math

class BreakBeam(object):
    """
        This class is used for interfacing with two photodiodes of the break beam sensor.
    """

    def __init__(self, inner_beam_pin, outer_beam_pin):
        self.inner_beam_pin = inner_beam_pin
        self.outer_beam_pin = outer_beam_pin
        self.INN = "In"
        self.OUTT = "Out"

        gpio.setmode(gpio.BOARD)
        gpio.setup(self.inner_beam_pin, gpio.IN)
        gpio.add_event_detect(self.inner_beam_pin, gpio.RISING, callback=self.break_direction_in)

        gpio.setmode(gpio.BOARD)
        gpio.setup(self.outer_beam_pin, gpio.IN)
        gpio.add_event_detect(self.outer_beam_pin, gpio.RISING, callback=self.break_direction_out)

        self.break_list = []

    def break_direction_in(self,dummy):
        ## Length of the shared list at the beginning of the callback
        lastlen = len(self.break_list)
        print(self.break_list)
        print("in")
        if lastlen==0:
            self.break_list.append(self.INN)
            time.sleep(1)
            if 1 < len(self.break_list):
                if self.break_list[-1]==self.INN:
                    print("Someone is derping.")
        else:
            if(self.break_list[-1]==self.OUTT):
                self.break_list.pop()
                print("Someone exited")
            else:
                self.break_list.pop()
                print("Someone is derping.")


    def break_direction_out(self,dummy):
        ## Length of the shared list at the beginning of the callback
        lastlen = len(self.break_list)
        print(self.break_list)
        print("out")
        if lastlen==0:
            self.break_list.append(self.OUTT)
            time.sleep(1)
            if 1 < len(self.break_list):
                if self.break_list[-1]==self.OUTT:
                    print("Someone is derping.")
        else:
            if(self.break_list[-1]==self.INN):
                self.break_list.pop()
                print("Someone entered")
            else:
                self.break_list.pop()
                print("Someone is derping.")

    def __del__():
        gpio.cleanup((self.outer_beam_pin,self.inner_beam_pin))


def main():
    X = BreakBeam(19,21)
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
