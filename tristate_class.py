from machine import Pin
import time

class Tristate:
    HIGH = 1
    LOW = -1
    OFF = 0
    
    def __init__(self, state = OFF):
        self.state = state


    def high(self):
        self.state = self.HIGH
    def low(self):
        self.state = self.LOW
    def off(self):
        self.state = self.OFF

    def to_pin(self, pin):
        if self.state == self.HIGH:
            pin.init(mode = Pin.OUT, value = 1 )     
        elif self.state == Tristate.LOW:
            pin.init(mode = Pin.OUT, value = 0 )
        else:
            pin.init(mode = Pin.IN) # hi-z
    def set_from_pin(self, pin):
        pass



def get_states(n,k,m):
    ''' return n Tristates where #k is HIGH and #m is LOW,
    otherwise OFF'''
    return tuple(Tristate(s) for s in tuple(Tristate.HIGH if i == k \
                 else Tristate.LOW if i == m \
                 else Tristate.OFF for i in range(n)))

def activate_pair(pinlist,k,m):
    ''' activate #k HIGH #m LOW in given list of Pin'''
    for i, pin in enumerate(pinlist):
        if i == k:
            Tristate(Tristate.HIGH).to_pin(pin)
        elif i == m:
            Tristate(Tristate.LOW).to_pin(pin)
        else:
            Tristate(Tristate.OFF).to_pin(pin)

def activate_states(pinlist,states):
    ''' activate list of Pin according to states in given '''
    for i, pin in enumerate(pinlist):
        states[i].to_pin(pin)

statelist = []
for m in range(3):
    for k in range(m):
        statelist += [get_states(3,m,k),get_states(3,k,m)]
print(statelist)
#statelist = [(0,1,2),(1,0,2),(0,2,1),(1,2,0),(2,0,1),(2,1,0)]
L0 = Pin(0,Pin.IN)
L1 = Pin(1,Pin.IN)
L2 = Pin(2,Pin.IN)
pinlist = [L0,L1,L2]
for _ in range(1):
    for states in statelist + list(reversed(statelist)):
        print(*(ts.state for ts in states))
        activate_states(pinlist, states)
        time.sleep(0.1)
time.sleep(2)
        
for m in range(3):
    for k in range(m):
        activate_pair(pinlist,m,k)
        time.sleep(1)
        activate_pair(pinlist,k,m)
        time.sleep(1)
