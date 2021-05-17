from smbus2 import SMBus
from mlx90614 import MLX90614
import time, random, os
import HCSR04

class OHandReader(object):
	LOCKED = -10
	UNLOCKED = 100
	VERIFICATION = 10
	DORMANT = 50
	STATE = DORMANT
	Temperature_list = []
	def __init__(self, trig_pin, echo_pin, i2c_bus = 1):
		
		self.bus = SMBus(i2c_bus)
		self.IRSens = MLX90614(self.bus)
		self.ProxSens= HCSR04.HCSR_04(trig_pin, echo_pin, self.IRSens.get_ambient())
		

	def verification(self):
		self.STATE = self.VERIFICATION
		self.ProxSens.set_temp(self.IRSens.get_ambient())
		#max_temp =300
		dist = 400
		count = 0
		Temperature_list = []
		while self.STATE == self.VERIFICATION:
			dist = self.ProxSens.distance()
			if ((dist>=400) or (dist<2.5)) and (count <300):
				count = count +1
			else:
				# Measuring the temperature
				#if dist <=50:
				#print(f"Distance = {dist:.3f} cm.")
				#print(f"Trial count = {count}")
				if	(dist <= 7) or (count >=300):
					self.Temperature_list.append(1.02* self.IRSens.get_object_1())
					time.sleep(0.25)
					self.Temperature_list.append(1.02* self.IRSens.get_object_1())
					time.sleep(0.25)
					self.Temperature_list.append(1.02* self.IRSens.get_object_1())
					time.sleep(0.25)
					self.Temperature_list.append(1.02* self.IRSens.get_object_1())
					time.sleep(0.25)
					self.Temperature_list.append(1.02* self.IRSens.get_object_1())
					time.sleep(0.25)
					max_temp = max(self.Temperature_list)
					self.Temperature_list.clear()
					
					
					if (37.5>max_temp>26):
						self.STATE = self.UNLOCKED
						print(f"\n######### \nYour skin temperature is {max_temp:.2f} C.")
						print("Skin temperature is approved! \nPlease look directly at the camera for mask check \n :) ")
						time.sleep(3)
						return self.STATE
					
					elif(max_temp >=37.5):
						self.STATE = self.LOCKED
						print(f"\n##########\nYour skin temperature is {max_temp:.2f} C.")
						print("THE DOOR IS LOCKED. BUZZZZZZZZ!!\n########")
						return self.STATE
				time.sleep(0.1)
				count =0
def main():
	try:
		os.nice(-5)
	except OSError:
		print("Process priority could not be decreased!")
		
	HandReader = OHandReader(12,18,1)
	#print(OHandReader.DORMANT)
	while True:
		print("\n########\nSomeone entered Doorfront area.") 
		print("Entering verification state.")	
		HandReader.verification()
		
		if HandReader.STATE == HandReader.UNLOCKED:
			print("Mask approved and the door is unlocked!")
			print("Waiting 10 seconds before locking the door...")
			time.sleep(10)
			print("\n#######\nPerson entered the building, Returning to sleep\n######")
		else:
			print("THE DOOR WILL REMAIN LOCKED UNTIL PERSON WITH FEVER LEAVES!")
			time.sleep(random.randint(3,9))
			print("The person left. Entering DORMANT state.")
			HandReader.STATE == HandReader.DORMANT
				
					
if __name__ == '__main__':
	main()
					
					
	
