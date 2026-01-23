import network
import time

# Create a WLAN object
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connect to WiFi
ssid = 'SOpenWrt24'
password = '2323232323'

print('Connecting to WiFi...')
wlan.connect(ssid, password)

# Wait for connection
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Check connection status
if wlan.status() != 3:
    print('Failed to connect')
else:
    print('Connected successfully')
    status = wlan.ifconfig()
    print('IP address:', status[0])
    
import socket
addr = socket.getaddrinfo('micropython.org', 80)[0][-1]
s = socket.socket()
s.connect(addr)
s.send(b'GET / HTTP/1.1\r\nHost: micropython.org\r\n\r\n')
data = s.recv(1000)
s.close()
print(type(data))
print(data)