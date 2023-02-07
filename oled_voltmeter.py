import machine, utime
from ssd1306 import SSD1306_I2C

i2c = machine.I2C(1,sda=machine.Pin(26), scl=machine.Pin(27))
oled = SSD1306_I2C(128, 32, i2c)
adc = machine.ADC(machine.Pin(28))

oled.fill(0)

while True:
    a = adc.read_u16()
    oled.fill(0)
    oled.text(str(a),0,0,1)
    oled.text(':'.join(str(s) for s in utime.localtime()[3:6]),0,10)
    oled.text('Stefan Karlsson',0,20)
    oled.show()
    utime.sleep_ms(100)
    