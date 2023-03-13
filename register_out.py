# Tänd gpio 0-7 genom att sätta register
import machine
import utime

sio_base = const(0xd0000000)
io_bank0_base = const(0x40014000)
gpio_oe = const(sio_base + 0x20)
gpio_out = const(sio_base + 0x10)
for k in range(8):
    machine.mem32[io_bank0_base + k*0x0008 + 0x0004] = 5 # funcsel = 5 sio
n = 0
machine.mem32[gpio_oe] |= 0xff # output enable gpio 0-7
try:
    while True:
        #print(n)
        machine.mem32[gpio_out] = n # set
        utime.sleep_ms(10)
        n = (n + 1) % 0x100
finally:
    print("Yup!")
    machine.mem32[gpio_out] = 0
    
        