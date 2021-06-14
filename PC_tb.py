from PeopleCounter import PeopleCounter
import RPi.GPIO as gpio
import time

X = PeopleCounter(23,24,21,22)
try:
    while True:
        time.sleep(1)
        print(f"BB1-(out/24 = {gpio.input(24)}, in/23 ={gpio.input(23)}), BB2-(out/22 = {gpio.input(22)}, in/21 = {gpio.input(21)})")
except KeyboardInterrupt:
        X.__del__()
        exit(1)
