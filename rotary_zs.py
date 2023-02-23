from machine import Pin
import utime

'''
Avkodar en rotationskodare.
Rotationsencoder till nolla med 100 nF parallellt
Inbyggd pullup på pico enligt uppgift ca 50 KOhm
Fungerar nära perfekt med lite felrättning
'''

pinA = Pin(5, Pin.IN, Pin.PULL_UP)
pinB = Pin(6, Pin.IN, Pin.PULL_UP)

def callback(pin):
    global interruptflag
    interruptflag = 1

irqA = pinA.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=callback)
irqB = pinB.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=callback)

interruptflag = 0
q = ()
bq = 0
position = 0
while True:
    if interruptflag:
        flags = irqA.flags() | (irqB.flags() >> 2)
        interruptflag = 0
        if flags == 0b1010:
            if bq & 0b011001011001 == 0b011001011001:
                #print('CCW')
                position -= 1
            elif bq & 0b100101010110 == 0b100101010110:
                #print('CW')
                position += 1
            print(f'{position:4} {bq:016b}')
            bq = 0
        elif flags != bq & 0b1111:
            bq = (bq << 4) | flags

                    