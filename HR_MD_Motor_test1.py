from ExitHandReader import ExitHandReader
from MaskDetector import MaskDetector
from OuterHandReader import OHandReader
from Buzzer import Buzzer
STATE = DORMANT
LOCKED = -10
UNLOCKED = 100
VERIFICATION = 10
DORMANT = 50
DENIED = 27


def main():
    try:
        os.nice(-15)
    except OSError:
        print("Process priority could not be decreased!")

    EntryHR= OHandReader(12,18,1)
    print("Entry Hand Reader Initialized!")
    ExitHR = ExitHandReader(32,31)
    print("Exit Hand Reader Initialized!")
    MD = MaskDetector(headless=False)
    print("Mask Detector Initialized!")
    door = Door()
    print("Door Initialized!")
    Buzzer = Buzzer(33)

    while True:
        STATE = DORMANT
        while STATE == DORMANT:
            if (ExitHR.read()):
                STATE = UNLOCKED
                print("The door is unlocked!")
                Buzzer.positiveresponse()
                door.exit()
                sleep(5)
            sleep(0.1)

        STATE = VERIFICATION

        while STATE == VERIFICATION:
            maskDetector.start_vid()
            result = exitHandReader.read()
            if(HAND_APPROVED == result):
                print("Checking face mask.")
                result = maskDetector.detect_mask()
                if result == "Mask":
                    print("Greetings. The door is unlocked.")
                    STATE = UNLOCKED
                    Buzzer.positiveresponse()
                    door.entrance()
                elif result == "ImproperMask":
                    print("Please wear your mask properly. When you do, have your hand measured again. Thank you!")
                    door.ringwarning()
                else:
                    print("You do not have a mask on! Please leave the door front area!")
                    door.ringerror()
                    STATE = LOCKED

        sleep(5)
