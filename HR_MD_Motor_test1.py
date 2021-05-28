from Buzzer import Buzzer
from Door import Door
import ExitHandReader
import MaskDetector
import OuterHandReader
import os
from time import sleep
import controller

HAND_APPROVED = 1
HAND_DENIED =0
NOT_HAND = 2

def main():
    try:
        os.nice(-15)
    except OSError:
        print("Process priority could not be decreased!")

    EntryHR= OuterHandReader.OHandReader(12,18,1)
    print("Entry Hand Reader Initialized!")
    ExitHR = ExitHandReader.ExitHandReader(32,31)
    print("Exit Hand Reader Initialized!")
    MD = MaskDetector.MaskDetector(headless=False)
    print("Mask Detector Initialized!")
    door = Door()
    print("Door Initialized!")
    B = Buzzer(33)



    while True:
        controller.STATE = controller.DORMANT
        while controller.STATE == controller.DORMANT:
            if (ExitHR.read()):
                controller.STATE = controller.UNLOCKED
                print("The door is unlocked!")
                B.positiveresponse()
                door.exit()
                sleep(1)
            sleep(0.1)

        controller.STATE = controller.VERIFICATION
        print("Verification state")
        MD.start_display()
        while controller.STATE == controller.VERIFICATION:
            result = EntryHR.read()
            if(HAND_APPROVED == result):
                print("Checking face mask.")
                result = MD.detect_mask()
                if result == "Mask":
                    print("Greetings. The door is unlocked.")
                    controller.STATE = controller.UNLOCKED
                    B.positiveresponse()
                    door.entrance()
                elif result == "ImproperMask":
                    print("Please wear your mask properly. When you do, have your hand measured again. Thank you!")
                    B.ringwarning()
                else:
                    print("You do not have a mask on! Please leave the door front area!")
                    B.ringerror()
                    controller.STATE = controller.LOCKED

        sleep(5)
if __name__ == '__main__':
    main()
