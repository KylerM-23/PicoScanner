from machine import Pin
import micropython
import time
import random

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

# when the pin changes, set cardin to true if switch pressed down, false otherwise
def cardChange(pinNum):
    global cardIn
    cardIn = True if limit_switch.value() else False

#limit switch on Pin 14 triggers interrupt on rising or falling edge
#limit_switch = Pin(14, Pin.IN, Pin.PULL_DOWN)
limit_switch = Pin(14, Pin.IN)
limit_switch.irq(handler=cardChange, trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING)

def read():
    print('Read')
    return True

def cleanup():
    print('Clean')

start = time.time()

while True:
    print(time.time() - start)
    time.sleep(0.1)
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
            