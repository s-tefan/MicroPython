

import array, time, utime
from machine import Pin
import rp2

NUM_LEDS = 12

'''
Neopixel WS2812 control
S-tefan 2023
PIO SM to be run at 20 MHz
put data (48 bit per led) on TX
'''
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW,\
             out_shiftdir=rp2.PIO.SHIFT_LEFT,\
             autopull=True,\
             pull_thresh=24)
def ws2812zs():
    set(y, 24)
    label('GO')
    out(x,1)
    jmp(not_x, 'LO') .side(1) [7]
    jmp('HI') .side(1) [7]
    label('LO')
    nop() .side(0) [7]
    label('HI')
    nop() .side(0) [7]
    nop()
    jmp(y_dec,'GO')

'''
code from
https://github.com/raspberrypi/pico-micropython-examples/blob/master/pio/pio_ws2812.py
PIO SM to be run at 8 MHz
put data (48 bit per led) on TX
'''
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW,\
             out_shiftdir=rp2.PIO.SHIFT_LEFT,\
             autopull=True,\
             pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1) .side(0) [T3 - 1]
    jmp(not_x, "do_zero") .side(1) [T1 - 1]
    jmp("bitloop") .side(1) [T2 - 1]
    label("do_zero")
    nop() .side(0) [T2 - 1]
    wrap()

sm = rp2.StateMachine(0, ws2812zs, freq=20_000_000, sideset_base=Pin(22))
#sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(22))
sm.active(1)
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

def spektrum():
    # g << 16 | r << 8 | b
    ar[0] = 0xff << 16
    ar[4] = 0xff << 8
    ar[8] = 0xff
    ar[6] = 0x7f << 8 | 0x7f
    ar[10] = 0x7f << 16 | 0x7f
    ar[2] = 0x7f << 16 | 0x7f << 8
    ar[3] = 0x3f << 16 | 0x7f << 8 | 0x00
    ar[1] = 0xbf << 16 | 0x3f << 8 | 0x00
    ar[11] = 0xff << 16 | 0x3f << 8 | 0x7f
    ar[9] = 0x7f << 16 | 0x00 << 8 | 0xff
    ar[7] = 0x00 << 16 | 0x7f << 8 | 0xff
    ar[5] = 0x00 << 16 | 0xff << 8 | 0x3f
    sm.put(ar,8)
    for k in range(1000):
        time.sleep_ms(100)
        a = ar[0]
        for k in range(NUM_LEDS-1):
            ar[k] = ar[k+1]
        ar[NUM_LEDS-1] = a
        sm.put(ar,8)

def fixpos(x):
    return (6 + x) % 12

def klocka_nu():
    ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    now = utime.localtime()
    print(now)
    ar[fixpos(now[3])] |= 0xff
    ar[fixpos(now[4] // 5)] |= 0xff << 16
    ar[fixpos(now[5] // 5)] |= 0xff << 8
    sec = fixpos(now[5])
    ar[fixpos(sec)] |= 0x0f << 16 | 0x0f << 8 | 0x0f
    sm.put(ar,8)

while True:
    klocka_nu()
    time.sleep_ms(1000//12)
    
    
    