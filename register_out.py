# Tänd gpio 0-7 genom att sätta register
import machine
import utime

sio_base = const(0xd0000000)
io_bank0_base = const(0x40014000)
gpio_oe = const(sio_base + 0x20) # output enable (1/0 -> out/in)
gpio_out = const(sio_base + 0x10) # output value (1/0 -> high/low)
for k in range(8):
    machine.mem32[io_bank0_base + k*0x08 + 0x04] = 5 # funcsel 5 -> sio på gpio 0--7
n = 0
machine.mem32[gpio_oe] |= 0xff # output enable gpio 0--7
try:
    while True:
        #print(n)
        machine.mem32[gpio_out] = n # set
        utime.sleep_ms(10)
        n = (n + 1) & 0xff
finally:
    # Släck när du går, är du snäll ...
    print("Nu stänger vi!")
    machine.mem32[gpio_out] = 0
    
        