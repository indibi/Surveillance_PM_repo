# Initiation of systems, objects and variables --
from Buzzer import Buzzer
from Door import Door
import sign
import ExitHandReader
import MaskDetector
import OuterHandReader
import os
import PeopleCounter
from time import sleep, time
import threading




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
    # global STATE
    # global LOCKED
    # global UNLOCKED
    # global VERIFICATION
    # global DORMANT
    # global DENIED

    #print(f"Thread identity = {threading.get_ident()}")
    while True:
        PC.STATE_LOCK.acquire()
        tmp_state = PC.STATE
        print(f"tmp_state = {PC.STATE}")
        PC.STATE_LOCK.release()
        while tmp_state == PC.DORMANT:
            PC.STATE_LOCK.acquire()
            if (PC.STATE == PC.DORMANT) and (PC.people_entrance >0):
                PC.STATE = PC.VERIFICATION
            PC.STATE_LOCK.release_lock()

            if(ExitHR.read()):
                PC.STATE_LOCK.acquire()
                if PC.STATE == PC.DORMANT:
                    PC.STATE = PC.UNLOCKED
                    PC.STATE_LOCK.release()
                    while ( B.positiveresponse() ==0):
                        pass
                    while (door.open() ==0):
                        pass
                    print("The door is unlocked!")
                else:
                    PC.STATE_LOCK.release()

            sleep(0.1)
            PC.STATE_LOCK.acquire()
            tmp_state = PC.STATE
            PC.STATE_LOCK.release()

        while tmp_state == PC.UNLOCKED:
            if (time()-door.state_tmstmp>8) and (door.state) and (PC.people_entrance == 0):
                PC.STATE_LOCK.acquire()
                PC.STATE = PC.DORMANT
                PC.STATE_LOCK.release()
                door.close()
                opsign.okayOff()

            sleep(0.1)
            PC.STATE_LOCK.acquire()
            tmp_state = PC.STATE
            PC.STATE_LOCK.release()

        while tmp_state == PC.VERIFICATION:
            print("State Verification")
            PC.STATE_LOCK.acquire()
            if (PC.STATE == PC.VERIFICATION) and (PC.people_inside > MAX_PEOPLE):
                PC.STATE = PC.LOCKED
                PC.STATE_LOCK.release()
                print("Too many people at the entrance. Please maintain social distancing.")
            elif (PC.STATE == PC.VERIFICATION) and (PC.people_entrance >1):
                PC.STATE = PC.LOCKED
                PC.STATE_LOCK.release()
            elif (PC.STATE == PC.VERIFICATION) and (PC.people_entrance ==0):
                PC.STATE = PC.DORMANT
                PC.STATE_LOCK.release()
            else:
                PC.STATE_LOCK.release()
                result = EntryHR.read()
                if(HAND_APPROVED == result):
                    print("Checking face mask.")
                    result = MD.last_label()
                    if result == "Mask":
                        print("Greetings. The door is unlocked.")
                        PC.STATE_LOCK.acquire()
                        PC.STATE = PC.UNLOCKED
                        PC.STATE_LOCK.release()
                        opsign.okayOn()
                        while (B.positiveresponse() ==0):
                            pass
                        while (door.open() ==0):
                            pass

                    elif result == "Improper Mask":
                        print("Please wear your mask properly. When you do, have your hand measured again. Thank you!")
                        opsign.imMaskErrorOn()
                        B.ringwarning()
                        sleep(0.5)
                        opsign.imMaskErrorOff()
                    else:
                        print("You do not have a mask on! Please leave the door front area!")
                        print(result)
                        # B.ringerror()
                        PC.STATE_LOCK.acquire()
                        PC.STATE = PC.DENIED
                        PC.STATE_LOCK.release()
                        opsign.noMaskErrorOn()
            sleep(0.1)
            PC.STATE_LOCK.acquire()
            tmp_state = PC.STATE
            PC.STATE_LOCK.release()


        while tmp_state == PC.DENIED:
            if PC.people_entrance > 0:
                while (B.ringwarning()==0):
                    pass
            else:
                print("Entrance cleared, going to Dormant state!")
                opsign.noMaskErrorOff()
                opsign.highErrorOff()
                opsign.fullErrorOff()
                PC.STATE_LOCK.acquire()
                PC.STATE = PC.DORMANT
                PC.STATE_LOCK.release()

            sleep(0.1)
            PC.STATE_LOCK.acquire()
            tmp_state = PC.STATE
            PC.STATE_LOCK.release()

        while tmp_state == PC.LOCKED:              ## >>  LOCKED STATE
            if PC.people_entrance == 0:
                PC.STATE_LOCK.acquire()
                PC.STATE = PC.DORMANT
                PC.STATE_LOCK.release()
            elif PC.people_entrance == 1:
                PC.STATE_LOCK.acquire()
                PC.STATE = PC.VERIFICATION
                PC.STATE_LOCK.release()
            else:
                while(B.ringerror()==0):
                    pass

            sleep(0.1)
            PC.STATE_LOCK.acquire()
            tmp_state = PC.STATE
            PC.STATE_LOCK.release()

if __name__ == '__main__':

    LOCKED = -10
    UNLOCKED = 100
    VERIFICATION = 10
    DORMANT = 50
    DENIED = 27


    HAND_APPROVED = 1
    HAND_DENIED =0
    NOT_HAND = 2
    MAX_PEOPLE = 2


    ExitHR = ExitHandReader.ExitHandReader(32,31)
    print("Exit Hand Reader Initialized!")

    door = Door()
    print("Door Initialized!")
    B = Buzzer(33)
    print("Buzzer Initialized!")
    PC = PeopleCounter.PeopleCounter(23,24,21,22, func=door.close)
    print("People Counter Initialized!")
    EntryHR= OuterHandReader.OHandReader(12,18,1, _get_state=PC._get_state)
    print("Entry Hand Reader Initialized!")
    MD = MaskDetector.MaskDetector(headless=False)
    print("Mask Detector Initialized!")
    opsign = sign.sign()
    opsign.fullErrorOn()
    sleep(0.2)
    opsign.highErrorOn()
    sleep(0.2)
    opsign.noMaskErrorOn()
    sleep(0.2)
    opsign.imMaskErrorOn()
    sleep(0.2)
    opsign.okayOn()
    sleep(1.2)
    opsign.fullErrorOff()
    sleep(0.2)
    opsign.highErrorOff()
    sleep(0.2)
    opsign.noMaskErrorOff()
    sleep(0.2)
    opsign.imMaskErrorOff()
    sleep(0.2)
    opsign.okayOff()

    main()
