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
		self.polling = True
		while (self.polling):
			gpio.output(self.trig_pin, 1)
			time.sleep(0.00001)
			gpio.output(self.trig_pin, 0)
			time.sleep(0.005)


		duration = self.t2 - self.t1
		distance = (duration * SonicSpeed)*50		# in centimeters
		return distance

	def timestamp(self,dummy):
		if(gpio.input(self.echo_pin)):
			self.t1=time.perf_counter()
		else:
			self.t2=time.perf_counter()
			self.polling = False


	def set_temp(self,temp):
		self.ambient_temp = temp
		#print(f"Ambient temperature is {temp:.2f}C")

	def __del__(self):
		gpio.cleanup((self.trig_pin, self.echo_pin))
