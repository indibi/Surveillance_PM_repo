import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

TRIG = 12
ECHO = 18

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
 
while True:	
	GPIO.output(TRIG, True)
	time.sleep(0.0001)
	GPIO.output(TRIG, False)

	while GPIO.input(ECHO) == False:
		start = time.time()
	while GPIO.input(ECHO) == True:
		end = time.time()

	net_time = end-start

	#cm
	distance = net_time /0.000058

	print(' Distance: {} cm' .format(distance))

GPIO.cleanup()
