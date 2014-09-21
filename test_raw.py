import serial
import struct
import time
import random

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=0)
ser.flushInput()
ser.flushOutput()

pixel = ["\x00\x00\x00"]
colours = pixel * 720
for x in range(720):
  output = "".join(colours)
  ser.write(output)
  colours.pop(0)
  R = random.random()*25
  G = random.random()*25
  B = random.random()*25
  pixel = struct.pack( "BBB", R,G,B)
  colours.append(pixel)
  time.sleep(0.05)

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


seedpixel = ["\xFF\xFF\xFF"]

seedpixel = ["\x00\x00\x1E"]
colours = seedpixel * 720
output = "".join(colours)
ser.write(output)
  
ser.write(720*seedpixel)
for x in range(1000):
  output = "".join(colours)
  ser.write(output)
  time.sleep(0.1)
  for y in range(50):
    index = random.random()*720
    pixel = colours.pop(index)
    R,G,B = struct.unpack("BBB", pixel)
    R = clamp(R + random.triangular(-5,5),0,30)
    G = clamp(G + random.triangular(-5,5),0,30)
    B = clamp(B + random.triangular(-5,5),0,30)
    #B = 100 - R - G
    pixel = struct.pack( "BBB", R,G,B)
    colours.insert(index,pixel)
