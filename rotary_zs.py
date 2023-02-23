from machine import Pin
import utime

'''
Avkodar en rotationskodare.
Rotationsencoder till nolla med 100 nF parallellt
Inbyggd pullup på pico enligt uppgift ca 50 KOhm
Fungerar inte långt från perfekt
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
position = 0
while True:
    if interruptflag:
        flags = irqA.flags(), irqB.flags()
        #print(flags)
        interruptflag = 0
        #print(q)
        if flags == (8,8):
            if q == (4,8,4,4,8,4):
                #print('CCW')
                position -= 1
            elif q == (8,4,4,4,4,8):
                #print('CW')
                position += 1
            print(position)
            q = ()
        else:
            q += flags
                    