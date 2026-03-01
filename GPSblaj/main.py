from machine import UART, Pin
import time
# Connect NEO-6M RX to GP0 and TX to GP1
# Initialize UART0 on GP0 (TX) and GP1 (RX)
# The NEO-6M defaults to a baud rate of 9600
gps_module = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

print("Searching for satellite fix...")

while True:
    if gps_module.any():
        # Read a line of NMEA data
        line = gps_module.readline()
        
        try:
            # Decode bytes to string
            data = line.decode('utf-8')
            print(line)
            
            # $GPRMC is the Recommended Minimum Navigation Information
            if "$GPRMC" in data:
                parts = data.split(',')
                
                # Check if the fix is valid ('A' = Active, 'V' = Void)
                if parts[2] == 'A':
                    timestamp = parts[1]
                    lat = parts[3]
                    lat_dir = parts[4]
                    lon = parts[5]
                    lon_dir = parts[6]
                    speed = parts[7]
                    
                    print(f"Time: {timestamp} | Lat: {lat}{lat_dir} | Lon: {lon}{lon_dir} | Speed: {speed} knots")
                else:
                    print("Waiting for valid GPS fix...")
                    
        except Exception as e:
            # Occasional decoding errors are common with serial data
            pass
            
    time.sleep(0.5)