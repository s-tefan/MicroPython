from machine import Pin
import time

def triset(pin, a):
    if a == 2:
        pin.init(mode = Pin.IN)
    else:
        pin.init(mode = Pin.OUT, value = a)

def stateset(pinlist, state):
    for k, pin in enumerate(pinlist):
        triset(pin, state[k])

statelist = [(0,1,2),(1,0,2),(0,2,1),(1,2,0),(2,0,1),(2,1,0)]
L0 = Pin(0,Pin.IN)
L1 = Pin(1,Pin.IN)
L2 =  Pin(2,Pin.IN)
pinlist = [L0,L1,L2]
for state in statelist:
    print(state)
    stateset(pinlist,state)
    time.sleep(1)

