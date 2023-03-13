"""
Register-demo
"""
from micropython import const
from machine import mem32
IO_BANK0_BASE   = const(0x40014000)
PADS_BANK0_BASE = const(0x4001c000)

def print_gpio_regs(gpionr):
    print(f'GPIO{gpionr:02}_STATUS: {mem32[IO_BANK0_BASE + (gpionr << 3)]:032b}')
    print(f'GPIO{gpionr:02}_CTRL:   {mem32[IO_BANK0_BASE + (gpionr << 3) + 4]:032b}')
    print(f'GPIO{gpionr:02}_PADS:   {mem32[PADS_BANK0_BASE + (gpionr << 2) + 4]:032b}')
    
"""
STATUS
26 IRQTOPROC interrupt to processors, after override is applied RO 0x0
24 IRQFROMPAD interrupt from pad before override is applied RO 0x0
19 INTOPERI input signal to peripheral, after override is applied RO 0x0
17 INFROMPAD input signal from pad, before override is applied RO 0x0
13 OETOPAD output enable to pad after register override is applied RO 0x0
12 OEFROMPERI output enable from selected peripheral, before register override is applied RO 0x0
9 OUTTOPAD output signal to pad after register override is applied RO 0x0
8 OUTFROMPERI output signal from selected peripheral, before register override is applied RO 0x0

CTRL
29:28 IRQOVER 0x0 → don’t invert the interrupt
0x1 → invert the interrupt
0x2 → drive interrupt low
0x3 → drive interrupt high
RW 0x0
17:16 INOVER 0x0 → don’t invert the peri input
0x1 → invert the peri input
0x2 → drive peri input low
0x3 → drive peri input high
RW 0x0
13:12 OEOVER 0x0 → drive output enable from peripheral signal selected by funcsel
0x1 → drive output enable from inverse of peripheral signal selected by funcsel
0x2 → disable output
0x3 → enable output
RW 0x0
9:8 OUTOVER 0x0 → drive output from peripheral signal selected by funcsel
0x1 → drive output from inverse of peripheral signal selected by funcsel
0x2 → drive output low
0x3 → drive output high
RW 0x0
4:0 FUNCSEL Function select. 31 == NULL. See GPIO function table for available functions. RW 0x1f
  0x05 for SIO

PADS
7 OD Output disable. Has priority over output enable from peripherals RW 0x0
6 IE Input enable RW 0x1
5:4 DRIVE Drive strength. 0x0 → 2mA, 0x1 → 4mA, 0x2 → 8mA, 0x3 → 12mA RW 0x1
3 PUE Pull up enable RW 0x0
2 PDE Pull down enable RW 0x1
1 SCHMITT Enable schmitt trigger RW 0x1
0 SLEWFAST Slew rate control. 1 = Fast, 0 = Slow RW 0x0
"""