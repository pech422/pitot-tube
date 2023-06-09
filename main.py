# Building of a digital Pitot - Static tube 
# UPV - ETSID, Aerospace engineering degree
# Last update 02/05/2023
# Álvaro Pérez Pecharromán, Julio Herranz Ibarra, Yoel Gomzález Denia, Ángel Caballero Miguel, Alexis Cantos Sempere, Pau Moreno Serra, Guillem Reig Malonda

from machine import Pin, I2C
from bmp085 import BMP180
import time
import math

i2c = I2C(1, sda = Pin(18), scl = Pin(19), freq = 1000) 
i2c2 = I2C(0, sda = Pin(16), scl = Pin(17), freq = 1000) 


bmp = BMP180(i2c)
bmp.oversample = 2
bmp.sealevel = 101325
bmp2 = BMP180(i2c2)
bmp2.oversample = 2
bmp2.sealevel = 101325
pres_ref = bmp.pressure*100

from machine import Pin

display_list = [10,11,14,13,12,9,8]
dotPin=15
display_obj = []

for seg in display_list:
    display_obj.append(Pin(seg, Pin.OUT))

dot_obj=Pin(dotPin, Pin.OUT)

arrSeg = [[1,1,1,1,1,1,0],\
          [0,1,1,0,0,0,0],\
          [1,1,0,1,1,0,1],\
          [1,1,1,1,0,0,1],\
          [0,1,1,0,0,1,1],\
          [1,0,1,1,0,1,1],\
          [1,0,1,1,1,1,1],\
          [1,1,1,0,0,0,0],\
          [1,1,1,1,1,1,1],\
          [1,1,1,1,0,1,1],\
          [1,0,0,1,1,1,0]]

def SegDisplay(toDisplay):
    numDisplay = int(toDisplay.replace(".", ""))
    for a in range(7):
        display_obj[a].value(arrSeg[numDisplay][a])
    if toDisplay.count(".") == 1:
        dot_obj.value(1)
    else:
        dot_obj.value(0)
        
acc1 = 0
acc2 = 0
        
for i in range(20):
    acc1 += bmp.pressure*100
    acc2 += bmp2.pressure*100
    SegDisplay(str(int(10)))
    time.sleep_ms(100)
    
offset1 = acc1/20
offset2 = acc2/20

while True: 
    tempC = bmp.temperature        
    pres_Pa = bmp.pressure*100 - offset1       
    pres_Pa2 = bmp2.pressure*100 - offset2
    altitude = bmp.altitude        
    temp_f= (tempC * (9/5) + 32)   
    speed = math.sqrt(2*(math.sqrt((pres_Pa-pres_Pa2)**2))/1000) *3.6
    print(str(pres_Pa)+" Pa   " +str(pres_Pa2)+" Pa   " +str(speed)+" km/h")
    if speed >= 20:
        speed = 19
    if speed >= 10:
        speed =- 10
        SegDisplay(str(int(speed)))
    else:
        SegDisplay(str(int(speed))+'.')
    time.sleep_ms(100) 