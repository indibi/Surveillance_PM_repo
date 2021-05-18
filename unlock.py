import RPi.GPIO as GPIO
import time
#define pins
pins[4] = [35,36,37,38] #yanyana olan pinler (ayarlanabilir)

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin,0)

fullstep_order =[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
# düz donüş
for i in range(200): #200 variable'ı değiştirilebilir açısında göre
    for fullstep in range(4):
        for pin in range(4):
            GPIO.output(pins[pin],fullstep_order[fullstep][pin])
            time.sleep(0.001)
time.sleep(25)
# ters dönüş
for i in range(200): #200 variable'ı değiştirilebilir açısında göre
    for fullstep in range(4):
        for pin in range(4):
            GPIO.output(pins[pin],fullstep_order[3-fullstep][pin])
            time.sleep(0.001)
