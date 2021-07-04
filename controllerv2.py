# Initiation of systems, objects and variables --
from Buzzer import Buzzer
from Door import Door
import sign
import ExitHandReader
import MaskDetector
import OuterHandReader
import os
#import PeopleCounter
from time import sleep, time
import threading
import RPi.GPIO as gpio


def main():
    print("inside main")
    try:
        os.nice(-15)
    except OSError:
        print("Process priority could not be decreased!")


    global EntryHR
    global ExitHR
    global MD
    global door
    global B
    global opsign

    people_inside =0
    print("people_inside = 0")
    while True:
        result = EntryHR.read2()
        print(f"Entry HR result = {result}")
        if ((result == HAND_DENIED) or (result == HAND_APPROVED)) and (people_inside>3):
            opsign.fullErrorOn()
            B.ringerror()
            print("Full inside")
            sleep(2)
            opsign.fullErrorOff()
        else:
            if(HAND_APPROVED == result):
                print("Checking face mask.")
                result = MD.reliable_last_label()
                if result == "Mask":
                    print("Greetings. The door is unlocked.")
                    people_inside+=1
                    opsign.okayOn()
                    while (B.positiveresponse() ==0):
                        pass
                    while (door.open() ==0):
                        pass
                    sleep(6)
                    while (door.close() ==0):
                        pass

                elif result == "Improper Mask":
                    print("Please wear your mask properly. When you do, have your hand measured again. Thank you!")
                    opsign.imMaskErrorOn()
                    while (B.ringwarning() ==0):
                        pass
                    sleep(0.5)
                    opsign.imMaskErrorOff()
                else:
                    print("You do not have a mask on! Please leave the door front area!")
                    print(result)
                    opsign.noMaskErrorOn()
                    while (B.ringerror() ==0):
                        pass
                    sleep(0.5)
                    opsign.imMaskErrorOff()

        if(ExitHR.read()):
            while ( B.positiveresponse() ==0):
                pass
            while (door.open() ==0):
                pass
            print("The door is unlocked!")
            if people_inside>0:
                people_inside-=1
            sleep(6)
            while ( door.close() ==0):
                pass


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

    #restart_button = 40
    #gpio.setmode(gpio.BOARD)
    #gpio.setup(restart_button, gpio.IN, pull_up_down=gpio.PUD_UP)
    #gpio.add_event_detect(restart_button, gpio.RISING, callback= restart, bouncetime=200)

    opsign = sign.sign()
    ExitHR = ExitHandReader.ExitHandReader(32,31)
    print("Exit Hand Reader Initialized!")
    input("EHR>>>>")
    opsign.okayOn()
    sleep(0.2)
    opsign.okayOff()
    door = Door()
    print("Door Initialized!")
    opsign.okayOn()
    sleep(0.2)
    opsign.okayOff()
    B = Buzzer(33)
    print("Buzzer Initialized!")
    opsign.okayOn()
    sleep(0.2)
    opsign.okayOff()
    #PC = PeopleCounter.PeopleCounter(23,24,21,22, func=door.close)
    #print("People Counter Initialized!")
    #opsign.okayOn()
    #sleep(0.2)
    #opsign.okayOff()
    EntryHR= OuterHandReader.OHandReader(12,18,1, _get_state=None)
    print("Entry Hand Reader Initialized!")
    opsign.okayOn()
    sleep(0.2)
    opsign.okayOff()
    MD = MaskDetector.MaskDetector(headless=False)
    print("Mask Detector Initialized!")
    opsign.okayOn()
    sleep(0.2)
    opsign.okayOff()
    opsign.fullErrorOn()
    sleep(0.2)
    opsign.fullErrorOff()

    main()
