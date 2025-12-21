from machine import Pin
import time
myLED = Pin(0, Pin.OUT)

morse_code = \
{
"A": ".-",
"B": "-...",
"C": "-.-.",
"D": "-..",
"E": ".",
"F": "..-.",
"G": "--.",
"H": "....",
"I": "..",
"J": ".---",
"K": "-.-",
"L": ".-..",
"M": "--",
"N": "-.",
"O": "---",
"P": ".--.",
"Q": "--.-",
"R": ".-.",
"S": "...",
"T": "-",
"U": "..-",
"V": "...-",
"W": ".--",
"X": "-..-",
"Y": "-.--",
"Z": "--..",
"0": "-----",
"1": ".----",
"2": "..---",
"3": "...--",
"4": "....-",
"5": ".....",
"6": "-....",
"7": "--...",
"8": "---..",
"9": "----.",
" ": "  "
}

def to_morse(text, code_table):
    return ''.join(code_table[c]+' ' for c in text)
    

def send_morse(pin, dotms, morsestr):
    pin.off()
    for c in morsestr:
        time.sleep_ms(dotms)
        if c == '.':
            pin.on()
            time.sleep_ms(dotms)
        elif c == '-' or c == '_':
            pin.on()
            time.sleep_ms(3*dotms)
        elif c == ' ':
            time.sleep_ms(dotms)
        pin.off()
        print(time.ticks_us())

#send_morse(myLED, 100, '...---...   -.- ..- -.- . _. -.-.--')
# three blanks for word separation (7 units off)

send_morse(myLED, 100, to_morse('STEFAN KARLSSON', morse_code))
