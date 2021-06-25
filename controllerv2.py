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
import RPi.GPIO as gpio

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


    while True:

        result = EntryHR.read()
        print(f"Entry HR result = {result}")
        if(HAND_APPROVED == result):
            print("Checking face mask.")
            result = MD.last_label()
            if result == "Mask":
                print("Greetings. The door is unlocked.")
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
                opsign.noMaskErrorOn()

        if(ExitHR.read()):
            while ( B.positiveresponse() ==0):
                pass
            while (door.open() ==0):
                pass
            print("The door is unlocked!")
            sleep(5)
            door.close()

        
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

    restart_button = 40
    gpio.setmode(gpio.BOARD)
    gpio.setup(restart_button, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.add_event_detect(restart_button, gpio.RISING, callback= restart, bouncetime=200)

    opsign = sign.sign()
    ExitHR = ExitHandReader.ExitHandReader(32,31)
    print("Exit Hand Reader Initialized!")
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
    PC = PeopleCounter.PeopleCounter(23,24,21,22, func=door.close)
    print("People Counter Initialized!")
    opsign.okayOn()
    sleep(0.2)
    opsign.okayOff()
    EntryHR= OuterHandReader.OHandReader(12,18,1, _get_state=PC._get_state)
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
