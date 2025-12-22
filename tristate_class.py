#Not working yet!
from machine import Pin
import time

class Tristate:
    HIGH = 1
    LOW = -1
    OFF = 0
    '''																																																																																																																																																																																																																																																																																																																																																																																																											ån	
    def __init__(self, state = Tristate.OFF):
        self.state = state
    '''

    def high(self):
        self.state = Tristate.HIGH

    def low(self):
        self.state = Tristate.LOW
    def off(self):
        self.state = Tristate.OFF

    def to_pin(self, pin):
        if self.state == Tristate.HIGH:
            pin.init(mode = Pin.OUT, value = 1 )     
        elif self.state == Tristate.LOW:
            pin.init(mode = Pin.OUT, value = 0 )
        else:
            pin.init(mode = Pin.IN) # hi-z
    def set_from_pin(self, pin):
        pass



def light(n,k,m):
    return tuple(Tristate.HIGH if i == k \
                 else Tristate.LOW if i == m \
                 else Tristate.OFF for i in range(n))
                 

def stateset(pinlist, state):
    for k, pin in enumerate(pinlist):
        triset(pin, state[k])
        
statelist = [light(3,k,m)  for m in range(3) for k in range(m)]
#statelist = [(0,1,2),(1,0,2),(0,2,1),(1,2,0),(2,0,1),(2,1,0)]
L0 = Pin(0,Pin.IN)
L1 = Pin(1,Pin.IN)
L2 = Pin(2,Pin.IN)
pinlist = [L0,L1,L2]
for _ in range(1):
    for state in statelist + list(reversed(statelist)):
        for pin in pinlist:
            state.to_pin(pin)
        time.sleep(0.1)
        

