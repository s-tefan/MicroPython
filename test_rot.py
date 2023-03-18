from machine import Pin
from micropython import const
import utime

pin_nrA, pin_nrB, pin_nrK, pin_nrVcc = 13, 12, 11, 10
sio_base = const(0xd0000000)
gpio_in = const(sio_base + 0x04) # input value (1/0 -> high/low)

pinVcc = Pin(pin_nrVcc, Pin.OUT)
pinA = Pin(pin_nrA, Pin.IN)
pinB = Pin(pin_nrB, Pin.IN)
pinK = Pin(pin_nrK, Pin.IN)
pinVcc.on()

#pinA.irq(trigger=Pin.IRQ_FALLING, handler=lambda x: print(x, 'falling', x.value(), pinB.value()))
while True:
    print(utime.ticks_ms(),pinA.value(),bin(machine.mem32[gpio_in]))
    utime.sleep_ms(10)
    pass
   