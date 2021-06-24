
import time, random, os
import HCSR04

OPEN_GATE = 1
NO_OPEN_GATE = 0
class ExitHandReader(object):
    def __init__(self, trig_pin, echo_pin):
        self.ProxSens= HCSR04.HCSR_04(trig_pin, echo_pin)

    def read(self):
        dist = self.ProxSens.distance()
        count =1
        ## Count counts the number of measurement trials that was done to
        ## get a healthy reading. Unhealthy ones are discarded.
        while((dist>=400) or (dist<2.5)):
            count = count+1
            time.sleep(0.01)
            dist = self.ProxSens.distance()
            if count == 60:
                break
            #print(f"Distance = {dist}")
            # Hand is within range
        if not((dist <= 8) or (count==60)):
            return NO_OPEN_GATE
            #print("Kimse yok ben kacar")
        #     #print("Finished")
        #     if (count!=60):
        #         #print("Object in range")
        #         #print(f"Distance = {dist:0.2f} cm")
        #         break
        dist = self.ProxSens.distance()
        count =1
        while((dist>=400) or (dist<2.5)):
            count = count+1
            time.sleep(0.01)
            dist = self.ProxSens.distance()
            if count == 60:
                break
            #print(f"Distance = {dist}")
            # Hand is within range
        if(dist <= 8) or (count==60):
            #print("Finished")
            if (count!=60):
                print("Object in range")
                print(f"Distance = {dist:0.2f} cm")
                return OPEN_GATE

        else:
            #print("Kimse yok ben kacar")
            return NO_OPEN_GATE
