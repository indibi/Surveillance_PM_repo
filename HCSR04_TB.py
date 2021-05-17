
import os
import matplotlib.pyplot as plt
from numpy import mean
import numpy as np
import RPi.GPIO as gpio
import time, math


class HCSR_04(object):
	''' This initializes a sonar proximity sensor that is sensitive to
	ambient temperature. It can
	'''
	def __init__(self, trig_pin, echo_pin, ambient_temp=25):
		self.trig_pin = trig_pin
		self.echo_pin = echo_pin
		self.ambient_temp = ambient_temp
		self.polling = False
		#self.last_duration = 0
		self.t1=0
		self.t2=0

		gpio.setmode(gpio.BOARD)
		gpio.setup(trig_pin, gpio.OUT, initial=gpio.LOW)
		gpio.setup(echo_pin, gpio.IN)
		gpio.add_event_detect(echo_pin, gpio.BOTH, callback=self.timestamp)


	def distance(self):
		SonicSpeed = 331.3 * math.sqrt(1+(self.ambient_temp/273.15)) # m/s
		inside_count =1
		self.polling = True
		while (self.polling):
			gpio.output(self.trig_pin, 1)
			time.sleep(0.00001)
			gpio.output(self.trig_pin, 0)
			time.sleep(0.005)
			#inside_count=inside_count+1


		duration = self.t2 - self.t1
		distance = (duration * SonicSpeed)*50		# in centimeters
		#print(f"Distance = {distance:.3f} cm.")
		#print(f"Inside count = {inside_count}")
		return distance

	def timestamp(self,dummy):
		if(gpio.input(self.echo_pin)):
			self.t1=time.perf_counter()
		else:
			self.t2=time.perf_counter()
			self.polling = False
		#else:
		#	self.t1=0
		#	self.t2=0


	def set_temp(self,temp):
		self.ambient_temp = temp
		print(f"Ambient temperature is {temp:.2f}C")

	def __del__(self):
		gpio.cleanup((self.trig_pin, self.echo_pin))

def main():
    try:
        os.nice(-20)
    except OSError:
        print("Process priority could not be increased!")

    try:
        sonar = HCSR_04(12,18,23)
        Testes = []
        Testcs = []
        Testds = []
        Testfps = []
        # Test for distances between 3-12 cm
        for i in range(3,13):
            input(">>> Waiting for user input to start the test for "+str(i)+" cm distance.")
            Testd =[]
            Testc =[]
            Teste =[]

            for j in range(30):
                count =1
                false_positive=0
                dist = sonar.distance()
                ## Count counts the number of measurement trials that was done to
                ## get a healthy reading. Unhealthy ones are discarded.
                while((dist>=400) or (dist<2.5)):
                    count = count+1
                    time.sleep(0.01)
                    dist = sonar.distance()

                if (i>7.5)and (dist<7.5):
                	false_positive = false_positive +1

                Testd.append(dist)
                Testc.append(count)
                Teste.append(dist-i)

                print(f"Distance = {dist:.3f} cm, Trial count = {count} times. ")
                time.sleep(0.2)
                count = 1

            Testfps.append(false_positive)
            Testes.append(Teste)
            Testcs.append(Testc)
            Testds.append(Testd)
            

        meane =[]
        maxe =[]
        meanc =[]
        maxc =[]

        for i in range(10):
        	meane.append(mean([abs(number) for number in Testes[i]]))
        	maxe.append(max(Testes[i]))
        	meanc.append(mean(Testcs[i]))
        	maxc.append(max(Testcs[i]))

        t = np.arange(3,13,1)
        plt.figure(1)
        plt.title("Distance measurement error stats")
        plt.subplot(211)
        plt.grid(True)
        plt.xlabel("Actual distance (cm)")
        plt.ylabel("Mean error (|cm|)")
        plt.plot(t,meane)

        plt.subplot(212)
        plt.grid(True)
        plt.xlabel("Actual distance (cm)")
        plt.ylabel("Max error (|cm|)")
        plt.plot(t, maxe)

        plt.show()

        plt.figure(2)
        plt.title("Distance measurement trial count stats")
        plt.subplot(211)
        plt.grid(True)
        plt.xlabel("Actual distance (cm)")
        plt.ylabel("Mean trial count")
        plt.plot(t,meanc)

        plt.subplot(212)
        plt.grid(True)
        plt.xlabel("Actual distance (cm)")
        plt.ylabel("Max trial count")
        plt.plot(t, maxc)

        plt.show()

        plt.figure(3)
        plt.title("Distance measurement false positives")
        plt.grid(True)
        plt.xlabel("Actual distance (cm)")
        plt.ylabel("Number of false positives")
        plt.plot(t,Testfps)
        plt.show()

    except KeyboardInterrupt:
        sonar.__del__()
        print("Cleaning Up!")

if __name__ == '__main__':
    main()
