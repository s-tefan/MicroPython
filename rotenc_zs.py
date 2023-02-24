from machine import Pin

class RotEnc:
    """Decodes a rotary encoder.

    Connect rotary encoder common to ground.
    The rotary encoder should be filtered for debouncing,
    for example by an RC filter.
    C between MC pin and ground. R between pin and encoder.
    Proposed values C = 100 nF, R = 1 KOhm.
    Further debouncing is achieved by error correcting in fixit().
    Stefan Karlsson, 2023
    """
    
    def __init__(self, pin_nrA, pin_nrB):
        self.pinA = Pin(pin_nrA, Pin.IN, Pin.PULL_UP)
        self.pinB = Pin(pin_nrB, Pin.IN, Pin.PULL_UP)
        self.irqA = self.pinA.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.callback)
        self.irqB = self.pinB.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.callback)
        self.interruptflag = 0
        self.value = 0
        self.bq = 0
        self.changed = False

    def callback(self, pin):
        #self.interruptflag = 1
        self.fixit()
        
    def fixit(self):
        flags = self.irqA.flags() | (self.irqB.flags() >> 2)
        if flags == 0b1010:
            if self.bq & 0b011001011001 == 0b011001011001:
                #CCW
                self.value -= 1
            elif self.bq & 0b100101010110 == 0b100101010110:
                #CW
                self.value += 1
            self.bq = 0
            self.changed = True
        elif flags != self.bq & 0b1111:
            self.bq = (self.bq << 4) | flags
        #self.interruptflag = 0

if __name__ == '__main__':
    """Test with encoder on pins 5 and 6 and print out values on change."""
    renc = RotEnc(5,6)
    while True:
        if renc.changed:
            print(renc.value)
            renc.changed = False
        
