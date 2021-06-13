import sign
from time import sleep

result = sign()
result.noMaskErrorOn()
sleep(1)
result.noMaskErrorOff()
result.imMaskErrorOn()
sleep(1)
result.imMaskErrorOff()
result.okayOn()
sleep(1)
result.okayOff()
result.highErrorOn()
sleep(1)
result.highErrorOff()
result.fullErrorOn()
sleep(1)
result.fullErrorOff()
