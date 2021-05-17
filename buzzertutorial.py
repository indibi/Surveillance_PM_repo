#Libraries
import RPi.GPIO as GPIO
from time import sleep
#Disable warnings (optional)
GPIO.setwarnings(False)
#Select GPIO mode
GPIO.setmode(GPIO.BCM)
#Set buzzer - pin 23 as output
trigger_pin=23
#Run forever loop
#while True:
#    GPIO.output(buzzer,GPIO.HIGH)
#    print ("Beep")
#    sleep(0.5) # Delay in seconds
#    GPIO.output(buzzer,GPIO.LOW)
#    print ("No Beep")
#    sleep(0.5)

buzzer = GPIO.PWM(trigger_pin, 1000) # Set frequency to 1 Khz
buzzer.start(10) # Set dutycycle to 10
#buzzer.ChangeDutyCycle(10)
#buzzer.ChangeFrequency(1000)

time.sleep(10)
buzzer.stop()
sys.exit()
