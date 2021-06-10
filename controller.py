# Initiation of systems, objects and variables --
from Buzzer import Buzzer
from Door import Door

import ExitHandReader
import MaskDetector
import OuterHandReader
import os
from time import sleep, time
import threading

LOCKED = -10
UNLOCKED = 100
VERIFICATION = 10
DORMANT = 50
DENIED = 27
STATE = DORMANT
STATE_LOCK = threading.Lock()

HAND_APPROVED = 1
HAND_DENIED =0
NOT_HAND = 2
MAX_PEOPLE = 20

EntryHR= OuterHandReader.OHandReader(12,18,1)
print("Entry Hand Reader Initialized!")
ExitHR = ExitHandReader.ExitHandReader(32,31)
print("Exit Hand Reader Initialized!")
MD = MaskDetector.MaskDetector(headless=False)
print("Mask Detector Initialized!")
door = Door()
print("Door Initialized!")
B = Buzzer(33)
print("Buzzer Initialized!")
PC = PeopleCounter.PeopleCounter(23,24,21,22)
print("People Counter Initialized!")
import PeopleCounter
def main():
    try:
        os.nice(-15)
    except OSError:
        print("Process priority could not be decreased!")


    global EntryHR
    global ExitHR
    global MD
    global door
    global B
    global PC
    global STATE
    global LOCKED
    global UNLOCKED
    global VERIFICATION
    global DORMANT
    global DENIED

    STATE = DORMANT

    while True:
        STATE_LOCK.acquire()
        tmp_state = STATE
        STATE_LOCK.release()

        while tmp_state == DORMANT:
            STATE_LOCK.acquire()
            if (STATE == DORMANT) and (PC.people_entrance >0):
                STATE = VERIFICATION
            STATE_LOCK.release_lock()

            if(ExitHR.read()):
                STATE_LOCK.acquire()
                if STATE == DORMANT:
                    STATE = UNLOCKED
                    STATE_LOCK.release()
                    while ( B.positiveresponse() ==0):
                        pass
                    while (door.open() ==0):
                        pass
                    print("The door is unlocked!")
                else:
                    STATE_LOCK.release()

            sleep(0.1)
            STATE_LOCK.acquire()
            tmp_state = STATE
            STATE_LOCK.release()

        while tmp_state == UNLOCKED:
            if (door.state_tmstmp-time()>5) and (door.state) and (PC.people_entrance == 0):
                STATE_LOCK.acquire()
                STATE = DORMANT
                STATE_LOCK.release()
                door.close()

            sleep(0.1)
            STATE_LOCK.acquire()
            tmp_state = STATE
            STATE_LOCK.release()

        while tmp_state == VERIFICATION:
            STATE_LOCK.acquire()
            if (STATE == VERIFICATION) and (PC.people_entrance >1):
                STATE = LOCKED
                STATE_LOCK.release()
            elif (STATE == VERIFICATION) and (PC.people_inside > MAX_PEOPLE):
                STATE = LOCKED
                STATE_LOCK.release()
                print("Too many people at the entrance. Please maintain social distancing.")
            else:
                STATE_LOCK.release()
                result = EntryHR.read()
                if(HAND_APPROVED == result):
                    print("Checking face mask.")
                    result = MD.last_label()
                    if result == "Mask":
                        print("Greetings. The door is unlocked.")
                        STATE_LOCK.acquire()
                        STATE = UNLOCKED
                        STATE_LOCK.release()
                        while (B.positiveresponse() ==0):
                            pass
                        while (door.open() ==0):
                            pass

                    elif result == "Improper Mask":
                        print("Please wear your mask properly. When you do, have your hand measured again. Thank you!")
                        B.ringwarning()
                    else:
                        print("You do not have a mask on! Please leave the door front area!")
                        # B.ringerror()
                        STATE_LOCK.acquire()
                        STATE = DENIED
                        STATE_LOCK.release()
            sleep(0.1)
            STATE_LOCK.acquire()
            tmp_state = STATE
            STATE_LOCK.release()


        while tmp_state == DENIED:
            if PC.people_entrance == 0:
                STATE_LOCK.acquire()
                STATE = DORMANT
                STATE_LOCK.release()
            else:
                while (B.ringwarning()==0):
                    pass

            sleep(0.1)
            STATE_LOCK.acquire()
            tmp_state = STATE
            STATE_LOCK.release()

        while tmp_state == LOCKED:              ## >>  LOCKED STATE
            if PC.people_entrance == 0:
                STATE_LOCK.acquire()
                STATE = DORMANT
                STATE_LOCK.release()
            elif PC.people_entrance == 1:
                STATE_LOCK.acquire()
                STATE = VERIFICATION
                STATE_LOCK.release()
            else:
                while(B.ringerror()==0):
                    pass

            sleep(0.1)
            STATE_LOCK.acquire()
            tmp_state = STATE
            STATE_LOCK.release()

if __name__ == '__main__':
    main()






#code here


#after this part infinity loop may be used
#(these processes execute many times)


# dormant state





#verification state







#deny state




#unlock state
