import board
import digitalio

class RotEnc:
    """Decodes a rotary encoder.
    CircuitPython version ported by ChatGPT. Not working...

    Connect rotary encoder common to ground.
    The rotary encoder should be filtered for debouncing,
    for example by an RC filter.
    C between MC pin and ground. R between pin and encoder.
    Internal pullup in CircuitPython is said to be ~40 kOhm
    Proposed values C = 100 nF, R = 1 kOhm.
    R needs to be small relative to pullup to bring signal low.
    Further debouncing is achieved by error correcting in fixit().
    Stefan Karlsson, 2023
    """
    
    def __init__(self, pin_nrA, pin_nrB):
        self.pinA = digitalio.DigitalInOut(getattr(board, f"GP{pin_nrA}"))
        self.pinA.direction = digitalio.Direction.INPUT
        self.pinA.pull = digitalio.Pull.UP
        self.pinB = digitalio.DigitalInOut(getattr(board, f"GP{pin_nrB}"))
        self.pinB.direction = digitalio.Direction.INPUT
        self.pinB.pull = digitalio.Pull.UP
        self.irqA = self.pinA.irq(trigger=digitalio.EdgeChange.RISING | digitalio.EdgeChange.FALLING, 
                                  handler=self.callback)
        self.irqB = self.pinB.irq(trigger=digitalio.EdgeChange.RISING | digitalio.EdgeChange.FALLING, 
                                  handler=self.callback)
        self.interruptflag = 0
        self.value = 0
        self.bq = 0
        self.changed = False

    def callback(self, pin):
        #self.interruptflag = 1
        self.fixit()
        
    def fixit(self):
        flags = self.irqA.edge() | (self.irqB.edge() >> 2)
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
            