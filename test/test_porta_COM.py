import serial
import time
import os

s = serial.Serial()
s.port = "COM9"
s.baudrate = 115200
s.dsrdtr = False
s.rtscts = False
s.dtr = False #reset high
s.rts = True #boot low
s.open()

print("Porta aperta")
time.sleep(0.1)

s.dtr = True #reset low
time.sleep(0.1)
s.rts = False #boot high
time.sleep(0.2)
s.dtr = False #reset high
time.sleep(0.2)


s.close()
