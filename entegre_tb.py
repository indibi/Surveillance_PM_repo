import MaskDetector
import OuterHandReader
import ExitHandReader

STATE = DORMANT
LOCKED = -10
UNLOCKED = 100
VERIFICATION = 10
DORMANT = 50
DENIED = 27


def main():
	try:
		os.nice(-5)
	except OSError:
		print("Process priority could not be decreased!")

    entryHandReader = OHandReader(12,18,1)
    print("Entry Hand Reader Initialized!")
    exitHandReader = ExitHandReader(32,31)
    print("Exit Hand Reader Initialized!")
    maskDetector = MaskDetector()
    print("Mask Detector Initialized!")

    while True:
        while STATE == DORMANT:
            if (exitHandReader.read()):
                STATE = UNLOCKED
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
                elif result == "ImproperMask":
                    print("Please wear your mask properly. When you do, have your hand measured again. Thank you!")
                else:
                    print("You do not have a mask on! Please leave the door front area!")
                    STATE = LOCKED
                    
