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
		#self.last_duration = 0
		#self.t1=0
		#self.t2=0

		gpio.setmode(gpio.BOARD)
		gpio.setup(trig_pin, gpio.OUT, initial=gpio.LOW)
		gpio.setup(echo_pin, gpio.IN)
		#gpio.add_event_detect(echo_pin, gpio.BOTH, callback=self.timestamp)
		
		
	def distance(self):
		SonicSpeed = 331.3 * math.sqrt(1+(self.ambient_temp/273.15)) # m/s	
		t1 =0		
		t2 =0
		gpio.output(self.trig_pin, 1)		
		#t1 = time.time()
		time.sleep(0.00001)
		gpio.output(self.trig_pin, 0)
		#t2 = time.time()		
		
		while(gpio.input(self.echo_pin)==0):
			t1 = time.time()
		
		while(gpio.input(self.echo_pin)==1):
			t2= time.time()
		
		#gpio.wait_for_edge(self.echo_pin, gpio.BOTH, timeout=22)
		#t1 = time.time()
		#gpio.wait_for_edge(self.echo_pin, gpio.BOTH, timeout=22)		
		#t2 = time.time()

		duration = t2 - t1
		
		distance = (duration * SonicSpeed)*50		# in centimeters
		print(f"Distance = {distance:.3f} cm.")
		return distance
		
	def timestamp(self,dummy):
		if(self.t1==0):
			self.t1=time.time()
		elif(self.t2==0):
			self.t2=time.time()
			self.last_duration = self.t2-self.t1
		else:
			t1=time.time()
			t2=0;

	
	def set_temp(self,temp):
		self.ambient_temp = temp
		print(f"Ambient temperature set to {temp}C")

	def __del__(self):
		gpio.cleanup((self.trig_pin, self.echo_pin))

def main():
	try:	
		sonar = HCSR_04(12,18,23)

		while True:
			sonar.distance()
			time.sleep(2)
	except KeyboardInterrupt:
		sonar._del_
		print("Cleaning Up!")


if __name__ == '__main__':
	main()
