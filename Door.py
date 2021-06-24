import RPi.GPIO as gpio
import time
import threading

class Door(object):
    def __init__(self, pins=[35,36,37,38]): # pinler disaridan da set edilebiliyor ama defaultu bu
        self.pins = pins  #yanyana olan pinler (ayarlanabilir)
        self.turn_number = 25 #dönme sayısı
        self.fullstep_order =[[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]]
        self.state = 0      # 0 = the door is  closed, 1 = the door is open
        self.state_tmstmp = time.time()
        gpio.setmode(gpio.BOARD)
        for pin in pins:
            gpio.setup(pin, gpio.OUT)
            gpio.output(pin,0)

        self.door_thread = threading.Thread(target= self._thread_loop)
        self._order_list = 0
        self._order_lock = threading.Lock()
        self.door_thread.start()


    def _open(self):
        self.state = 1
        self.state_tmstmp = time.time()
        for i in range(self.turn_number):
            for fullstep in range(4):
                for pin in range(4):
                    gpio.output(self.pins[pin],self.fullstep_order[fullstep][pin])
                    time.sleep(0.002)

    def _close(self):
        self.state = 0
        self.state_tmstmp = time.time()
        for i in range(self.turn_number):
            for fullstep in range(4):
                for pin in range(4):
                    gpio.output(self.pins[pin],self.fullstep_order[3-fullstep][pin])
                    time.sleep(0.002)

    def entrance(self):
    # düz donüş
        self._open()
    #break beam kodu---------
        time.sleep(6)
    # ters dönüş
        self._close()

    def exit(self):
        # düz donüş
        self._open()
        #break beam kodu-----
        time.sleep(6)
        # ters dönüş
        self._close()

    def _thread_loop(self):
        while True:
            self._order_lock.acquire()
            a = self._order_list
            self._order_list=0
            self._order_lock.release()
            if a== 1:
                self._open()
            elif a == 2:
                self._close()
            else:
                time.sleep(0.4)

    def open(self):
        self._order_lock.acquire()
        if self._order_list ==0:
            self._order_list = 1
            self._order_lock.release()
            return 1
        else:
            self._order_lock.release()
            return 0

    def close(self):
        self._order_lock.acquire()
        if self._order_list ==0:
            self._order_list = 2
            self._order_lock.release()
            return 2
        else:
            self._order_lock.release()
            return 0


    def __del__(self):
        gpio.cleanup(self.pins)
