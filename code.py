from machine import Pin
import machine
import micropython
import time
from mfrc522 import MFRC522

'''
The state variable keeps track of the current state of the device.
It is used for checking what the previous state was.
State 0: No Card - Waiting 
State 1: Card Inserted - Reading
State 2: Card Inserted - Waiting
State 3: No Card - Cleanup
'''

state = 0
cardIn = False
success = False
target = 3567068812 
reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)
start = time.time()
reader.init()
limit_switch = Pin(14, Pin.IN, Pin.PULL_DOWN)
int_avaliable = True
# when the pin changes, set cardin to true if switch pressed down, false otherwise
def changeState():
    global cardIn
    cardIn = True if limit_switch.value() else False

def accident():
    original = limit_switch.value()
    time.sleep(10)
    if (limit_switch.value() == original):
        changeState()
    
def cardChange(pinNum):
    global int_avaliable
    if not int_avaliable:
        return
    int_avaliable = False
    limit_switch.irq(handler=None, trigger = 0)
    print("Card change")
    time.sleep(.02)
    accident()
    print("Almost")
    limit_switch.irq(handler=cardChange, trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING)
    print("Over")
    

#limit switch on Pin 14 triggers interrupt on rising or falling edge
limit_switch.irq(handler=cardChange, trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING)

outputBit = Pin(15, Pin.OUT)
outputBit.value(0)

RGB = [Pin(11, Pin.OUT), Pin(12, Pin.OUT), Pin(13, Pin.OUT)]

def RGBOutput(color):
    for i in range(len(RGB)):
        RGB[i].value(color[i])
        
def read():
    hits = 0
    for i in range(6):
        (stat, tag_type) = reader.request(reader.REQIDL)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                card = int.from_bytes(bytes(uid),"little",False)
                print("CARD ID: "+str(card))
                if (card == target):
                    hits += 1 
    result = True if (hits >= 3) else False
    
    if result:
        RGBOutput([0,0,1])
        outputBit.value(1)
    else:
        RGBOutput([1,0,0])
    return result

def cleanup():
    print('Clean')

while True:
    #print(time.time() - start)
    time.sleep(0.05)
    if cardIn:
        if state == 0:
            state = 1
        elif state == 1:
            print("Reading")
            success = read()
            state = 2
        elif state == 2:
            print('Wait After Read')
            int_avaliable = True
        else:
            print("This should not happen uh oh.")
            
    else:
        outputBit.value(0)
        if success:
            state = 3
        else:
            state = 0
            
        if state == 0:
            int_avaliable = True
            RGBOutput([0,1,0])
            print('Nothing')
        
        elif state == 3:
            cleanup()
            success = False
            state = 0
        else:
            print("Hmm, idk how you did this.")
