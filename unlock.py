import RPi.GPIO as gpio
import time


class Door(object):
    def __init__(self, pins=[35,36,37,38]): # pinler disaridan da set edilebiliyor ama defaultu bu
        self.pins = pins  #yanyana olan pinler (ayarlanabilir)
        self.turn_number = 200 #dönme sayısı
        self.fullstep_order =[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        for pin in pins:
            gpio.setup(pin, gpio.OUT)
            gpio.output(pin,0)


    def entrance(self):
    # düz donüş
        for i in range(self.turn_number):
            for fullstep in range(4):
                for pin in range(4):
                    gpio.output(self.pins[pin],self.fullstep_order[fullstep][pin])
                    time.sleep(0.001)

    #break beam kodu---------
        time.sleep(10)
    # ters dönüş
        for i in range(self.turn_number):
            for fullstep in range(4):
                for pin in range(4):
                    gpio.output(self.pins[pin],self.fullstep_order[3-fullstep][pin])
                    time.sleep(0.001)
    def exit(self):
        # düz donüş
            for i in range(self.turn_number):
                for fullstep in range(4):
                    for pin in range(4):
                        gpio.output(self.pins[pin],self.fullstep_order[fullstep][pin])
                        time.sleep(0.001)
        #break beam kodu-----
        time.sleep(10)
        # ters dönüş
            for i in range(self.turn_number):
                for fullstep in range(4):
                    for pin in range(4):
                        gpio.output(self.pins[pin],self.fullstep_order[3-fullstep][pin])
                        time.sleep(0.001)

    def __del__(self):
        gpio.cleanup(self.pins)
