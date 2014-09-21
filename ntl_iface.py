import serial
import struct
import time
import binascii
import pygame

class NTL:
  def __init__(self, port="/dev/ttyACM0"):
    #Open serial port as with default blocking read
    self.ser = serial.Serial(port, 115200, timeout=None)
    self.ser.flushInput()
    self.ser.flushOutput()
    self.draw_finished = True
  def draw_surface(self, surface):
    if (self.draw_finished == True):
      #self.draw_finished = False
      #print "Draw", time.time()
      (width, height) = surface.get_size()
      if (width, height) != (24,30):
        raise Exception("Erm wrong size dude")
      #Note : Bottom of first column is clocked in first
      pixels = []
      for x in range(width):
        if x%2:
          yrange = reversed(range(height))
        else:
          yrange = range(height)
        for y in yrange:
          pixels.append(struct.pack( "BBB", surface.get_at((x,y))[0],
                                            surface.get_at((x,y))[1], 
                                            surface.get_at((x,y))[2]) )
      self.ser.write( "".join(pixels) )
    else:
      pass
      #raise Exception("*** Drawing too fast yo!")
  def run(self):
    while True:
      data = self.ser.read(1)
      
      if data == "D":
        pass
      elif data == "F":
        self.draw_finished = True
        #print "Done", time.time()
      else:
        self.ser.flushInput()
