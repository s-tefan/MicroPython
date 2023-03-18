from machine import Pin
import utime
class RotEnc:
    """Decodes a rotary encoder.

    Connect rotary encoder common to ground.
    The rotary encoder should be filtered for debouncing,
    for example by an RC filter.
    C between MC pin and ground. R between pin and encoder.
    Internal pullup in pico is said to be ~50 kOhm
    Proposed values C = 100 nF, R = 1 kOhm.
    R needs to be small relative to pullup to bring signal low.
    Further debouncing is achieved by error correcting in fixit().
    Stefan Karlsson, 2023
    """
    
    def __init__(self, pin_nrA, pin_nrB):
        self.pinA = Pin(pin_nrA, Pin.IN, Pin.PULL_UP)
        self.pinB = Pin(pin_nrB, Pin.IN, Pin.PULL_UP)
        #self.pinA = Pin(pin_nrA, Pin.IN)
        #self.pinB = Pin(pin_nrB, Pin.IN)
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

sio_base = const(0xd0000000)
io_bank0_base = const(0x40014000)
gpio_oe = const(sio_base + 0x20) # output enable (1/0 -> out/in)
gpio_oe_set = const(sio_base + 0x24) # set out (1/0 -> out/in)
gpio_oe_clr = const(sio_base + 0x28) # set in (1/0 -> out/in)
gpio_in = const(sio_base + 0x04) # input value (1/0 -> high/low)
gpio_out = const(sio_base + 0x10) # output value (1/0 -> high/low)
gpio_out_xor = const(sio_base + 0x1c) # output value (1/0 -> high/low)
gpio_out_set = const(sio_base + 0x14) # output value (1/0 -> high/low)
gpio_out_clr = const(sio_base + 0x18) # output value (1/0 -> high/low)

for k in range(8):
    machine.mem32[io_bank0_base + k*0x08 + 0x04] = 5 # funcsel 5 -> sio på gpio 0--7

n = 0

n = 255
machine.mem32[gpio_oe_set] = 0xff # 1 -- 7 output

print(machine.mem32[gpio_oe])

renc = RotEnc(13,12)
pinv = Pin(10, Pin.OUT)
pinv.on()
while True:
    #utime.sleep_ms(10)
    #print(bin(machine.mem32[gpio_in]))
    if renc.changed:
        print(renc.value)
        machine.mem32[gpio_out_clr] = 0xff
        machine.mem32[gpio_out_set] = 0x1 << (renc.value % 8)
        renc.changed = False
    

