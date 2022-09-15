from machine import Pin
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
target = 209451056 
reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)
start = time.time()
reader.init()

# when the pin changes, set cardin to true if switch pressed down, false otherwise
def cardChange(pinNum):
    global cardIn
    cardIn = True if limit_switch.value() else False

#limit switch on Pin 14 triggers interrupt on rising or falling edge
limit_switch = Pin(14, Pin.IN, Pin.PULL_DOWN)
#limit_switch = Pin(14, Pin.IN)
limit_switch.irq(handler=cardChange, trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING)

outputBit = Pin(15, Pin.OUT)
outputBit.value(0)

def read():
    hits = 0
    for i in range(5):
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
        outputBit.value(1)
    
    return result

def cleanup():
    print('Clean')

while True:
    print(time.time() - start)
    time.sleep(0.05)
    
    if cardIn:
        if state == 0:
            state = 1
        elif state == 1:
            success = read()
            state = 2
        elif state == 2:
            print('Wait After Read')
        else:
            print("This should not happen uh oh.")
            
    else:
        outputBit.value(0)
        if success:
            state = 3
        else:
            state = 0
            
        if state == 0:
            print('Nothing')
        
        elif state == 3:
            cleanup()
            success = False
            state = 0
        else:
            print("Hmm, idk how you did this.")
            