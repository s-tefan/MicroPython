from machine import Pin, SPI
from time import sleep, sleep_us
'''Exempel på att styra en MCP4921 DAC frå rpi pico'''

spi = SPI(0, 20_000_000, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
val = 0
cs = Pin(5,Pin.OUT,value=1)
led = Pin('LED', Pin.OUT)

while True:
  if not val:
    led.value(not led.value())
  txdata = (0x3000 | val).to_bytes(2, 'big')
  cs(0)
  #sleep_us(1)
  spi.write(txdata)
  #sleep_us(1)
  cs(1)
  sleep(0.001)
  val += 4
  val %= 0x1000
