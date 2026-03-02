import machine
import sys
import select

# Configure UART - using UART0 on GPIO0 (TX) and GPIO1 (RX)
# Change to UART1 + GPIO4/5 if needed
br =115200

uart = machine.UART(0, baudrate=br, tx=machine.Pin(0), rx=machine.Pin(1))

# USB serial (stdin/stdout)
usb = sys.stdin.buffer

print("UART <-> USB Serial bridge ready")
print(f"UART0: TX=GPIO0, RX=GPIO1, Baud={br}")

while True:
    # Check for data from USB → send to UART
    if select.select([sys.stdin], [], [], 0)[0]:
        data = usb.read(64)
        if data:
            uart.write(data)

    # Check for data from UART → send to USB
    if uart.any():
        data = uart.read(uart.any())
        if data:
            sys.stdout.buffer.write(data)


