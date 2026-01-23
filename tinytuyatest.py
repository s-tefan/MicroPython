import tinytuya



devices = tinytuya.deviceScan()
print(devices)

'''

# Connect to Device
d = tinytuya.OutletDevice(
    dev_id='DEVICE_ID_HERE',
    address='IP_ADDRESS_HERE',      # Or set to 'Auto' to auto-discover IP address
    local_key='LOCAL_KEY_HERE', 
    version=3.3)

# Get Status
data = d.status() 
print('set_status() result %r' % data)

# Turn On
d.turn_on()

# Turn Off
d.turn_off()

'''