from ExitHandReader import ExitHandReader
from MaskDetector import MaskDetector
from OuterHandReader import OHandReader



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

    STATE = DORMANT
    while True:
        while STATE == DORMANT:
            if (ExitHR.read()):
                STATE = UNLOCKED
                door.exit()
                print("The door is unlocked!")
                sleep(5)
            sleep(0.1)

        while STATE == VERIFICATION:
            maskDetector.start_vid()
            result = exitHandReader.read()
            if(HAND_APPROVED == result):
                print("Checking face mask.")
                result = maskDetector.detect_mask()
                if result == "Mask":
                    print("Greetings. The door is unlocked.")
                    STATE = UNLOCKED
					door.entrance()
                elif result == "ImproperMask":
                    print("Please wear your mask properly. When you do, have your hand measured again. Thank you!")
                else:
                    print("You do not have a mask on! Please leave the door front area!")
                    STATE = LOCKED
