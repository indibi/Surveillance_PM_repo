from smbus2 import SMBus
from mlx90614 import MLX90614
import time

def main():
	
	bus = SMBus(1)		# This is the I2C bus used
	
	IRSens = MLX90614(bus)
	
	while True:
		#print(f"Ambient Temperature = {IRSens.get_ambient():.2f}")
		print(f"     IR Temperature = {1.02*IRSens.get_object_1():.2f}")
		# print(f"T_obj2 = {IRSens.get_object_2()}")
		time.sleep(0.3)


if __name__ == '__main__':
	main()
