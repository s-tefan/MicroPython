from machine import Timer, Pin
import utime
timer = Timer(period=1000, mode=Timer.PERIODIC, callback=lambda t:print(utime.ticks_us(),utime.ticks_us()))
timer2 = Timer(period=5000, mode=Timer.PERIODIC, callback=lambda t:print("Raj!",utime.ticks_us(),utime.ticks_us()))

