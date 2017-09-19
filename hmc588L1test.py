#!/usr/bin/python
# s.pursell use terminal command python3 hmc5883Ltest.py > outputfilename.dat to send output to a file

import smbus
import time
import math

bus = smbus.SMBus(1)

address = 0x1e

#print ("I am here 1")

def read_byte(adr):
    return bus.read_byte_data(address, adr)
#    print ("I am read_byte")
    
def read_word(adr):
#    print ("I am read_word")
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
#    print ("I am read_word_2c")
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
    
def write_byte(adr, value):
#    print ("I am write_byte")
    bus.write_byte_data(address, adr, value)
    
#write_byte(0, 0b01110000) #Set to 8 samples @ 15Hz
#write_byte(0, 0b00010000) #Set to 1 sample @ 15Hz
write_byte(0, 0b00001000) #Set to 1 sample @ 3Hz

write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)

write_byte(2, 0b00000000) # Continuous sampling

scale = 0.92

for i in range(0,500):
     x_out = read_word_2c(3) * scale
     y_out = read_word_2c(7) * scale 
     z_out = read_word_2c(5) * scale

     bearing = math.atan2(y_out, x_out)
    
     #print ("I am here 2")

     if (bearing < 0):
         bearing += 2 * math.pi
       
     print ("Bearing:", math.degrees(bearing))
     print ("x-out x-scaled", x_out, (x_out * scale))
     print ("y-out y-scaled", y_out, (y_out * scale))
     print ("z-out z-scaled", z_out, (z_out * scale)) 
     print ()
     
     time.sleep(5)
     
     
print ("Finished with 500 samples")

#print ("I am at the end")  
