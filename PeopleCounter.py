import RPi.GPIO as gpio
import time, math, threading, sys
import controller

class BreakBeam(object):
    def __init__(self, BB_in, BB_out, BB_callback):
        self.BB_in=BB_in
        self.BB_out=BB_out
        self.BB_t_IN=(0,time.time())    # (last state, timestamp of record)
        self.BB_t_OUT=(0,time.time())
        self.LOCK = threading.Lock()     ## Mutex lock for timer synchronization
        gpio.setmode(gpio.BOARD)
        gpio.setup(BB_in, gpio.IN)
        gpio.add_event_detect(BB_in, gpio.RISING, callback=BB_callback)
        gpio.setup(BB_out, gpio.IN)
        gpio.add_event_detect(BB_out, gpio.RISING, callback=BB_callback)

    def __del__(self):
        gpio.cleanup((self.BB_in, self.BB_out))


class PeopleCounter(object):
    def __init__(self, BB1_in,BB1_out, BB2_in,BB2_out, func = None):
        self.BB1 = BreakBeam(BB1_in,BB1_out, self.break_1)
        self.BB2 = BreakBeam(BB2_in,BB2_out, self.break_2)
        self.people_inside=0
        self.people_entrance=0
        self.LOCK = threading.Lock()
        self.LOCKED = -10
        self.UNLOCKED = 100
        self.VERIFICATION = 10
        self.DORMANT = 50
        self.DENIED = 27
        self.STATE = self.DORMANT
        self.STATE_LOCK = threading.Lock()

    def break_2(self, channel):
        self.BB2.LOCK.acquire_lock()
        t = time.time()
        if(channel==self.BB2.BB_out): ## If the trigger was outer pin
            x,y = self.BB2.BB_t_IN  ## get the last flag records
            print("BB2 out")
            if(x):                      ## If the inner beam was already broken
                if((t-y)<1):                ## If the timing was right. A person exited the building
                    self.LOCK.acquire_lock()   ## Get the mutex of people counters
                    self.people_inside -= 1    ## Decrement inside counter
                    self.people_entrance +=1   ## Increment the entrance counter
                    self.LOCK.release_lock()   ## Release the mutex of people counters
                    print(f"Someone exit the building! Inside count={self.people_inside}, Outside count={self.people_entrance}")
                    self.BB2.BB_t_IN=(0,t)     ## Clear the flags after count
                    self.BB2.BB_t_OUT=(0,t)
                else:                       ## If the set inner beam flag was too old ignore it and refresh the flags
                    self.BB2.BB_t_IN=(0,t)
                    self.BB2.BB_t_OUT=(1,t)
            else:                   ## If the inner beam was not already set
                self.BB2.BB_t_IN=(0,t)
                self.BB2.BB_t_OUT=(1,t) ## Record the event with timestamp

        if(channel==self.BB2.BB_in): ## If the trigger was inner pin
            x,y = self.BB2.BB_t_OUT ## get the last flag records
            print("BB2 in")
            if(x):                      ## If the outer pin was already broken
                if((t-y)<1):                ## If the timing was right A person entered the building
                    self.LOCK.acquire_lock()
                    self.people_inside +=1
                    self.people_entrance-=1
                    print(f"Someone entered the building! Inside count={self.people_inside}, Outside count={self.people_entrance}")
                    self.LOCK.release_lock()
                    self.BB2.BB_t_IN=(0,t)     ## Clear the flags after count
                    self.BB2.BB_t_OUT=(0,t)
                else:                       ## If the set inner beam was too old, ignore it and refresh the flags
                    self.BB2.BB_t_IN=(1,t)
                    self.BB2.BB_t_OUT=(0,t)
            else:                       ## If the outer pin wasnt previously broken
                self.BB2.BB_t_IN=(1,t)
                self.BB2.BB_t_OUT=(0,t) ## Record the event with timestamp
        self.BB2.LOCK.release_lock() ## Release the clock locks

    def break_1(self, channel):
        self.BB1.LOCK.acquire_lock()
        t = time.time()
        if(channel==self.BB1.BB_out):   ## If the trigger was outer pin
            (x,y) = self.BB1.BB_t_IN
            print("BB1-out")
            if(x):                          ## If inner beam was already broken
                if((t-y)<1):                    ## If the timing was right. A person left entrance
                    self.LOCK.acquire_lock()        ## Get mutex of people counts
                    self.people_entrance -=1
                    print(f"Someone left entrance area! People inside count={self.people_inside}, People at entrance count={self.people_entrance}")
                    self.LOCK.release_lock()        ## Release mutex of people counts
                    self.BB1.BB_t_IN = (0,t)
                    self.BB1.BB_t_OUT=(0,t)
                else:                       ## If the set inner beam flag was too old ignore it
                    self.BB1.BB_t_IN =(0,t)
                    self.BB1.BB_t_OUT =(1,t)
            else:                       ## If the inner beam was not set
                self.BB1.BB_t_IN =(0,t)
                self.BB1.BB_t_OUT=(1,t)

        if(channel==self.BB1.BB_in): ## If the trigger was inner pin
            (x,y) = self.BB1.BB_t_OUT
            print("BB1-in")
            if(x):          ## If outer beam was already broken
                if((t-y)<1):     ## Timing was right. A person entered entrance
                    self.LOCK.acquire_lock()
                    self.people_entrance+=1
                    print(f"Someone entered entrance area! People inside count={self.people_inside}, People at entrance count={self.people_entrance}")
                    print(f"Thread identity = {threading.get_ident()}")
                    self.STATE_LOCK.acquire()
                    print("State Lock acquired")
                    print(f"State = {controller.STATE}")
                    if self.STATE == self.UNLOCKED:
                        self.STATE = self.LOCKED
                        while (controller.door.close() ==0):
                            pass
                    self.STATE_LOCK.release()
                    print("State Lock released")
                    self.LOCK.release_lock()
                    self.BB1.BB_t_IN = (0,t)
                    self.BB1.BB_t_OUT=(0,t)
                else:       ## If outer beam flag was too old, ignore it
                    self.BB1.BB_t_IN = (1,t)
                    self.BB1.BB_t_OUT=(0,t)
            else:         ## If the outer beam was not broken
                self.BB1.BB_t_IN =(1,t)
                self.BB1.BB_t_OUT=(0,t)

        self.BB1.LOCK.release_lock()


# def main():
#     X = PeopleCounter(19,21)
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         X.__del__()
#         exit(1)
#
# if __name__=='__main__':
#     main()
