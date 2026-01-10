from machine import Pin
from time import sleep

led = Pin('LED', Pin.OUT)
gp22 = Pin(22, Pin.OUT)
print('Blinking LED Example')

while True:
  led.value(not led.value())
  sleep(0.1)
  gp22.value(not gp22.value())
  sleep(0.1)
