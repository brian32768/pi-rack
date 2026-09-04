import select
import sys
import time
from machine import Pin, UART

# Create an instance of a polling object 
usb = select.poll()
# Register sys.stdin (standard input) for monitoring read events with priority 1
usb.register(sys.stdin,1)

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
uart.init(bits=8, parity=None, stop=1)

led=Pin("LED",Pin.OUT)

i = 5
while i>0 :
    led.on()
    time.sleep(.1)
    led.off()
    time.sleep(.1)
    i -= 1

while True:
      
    if usb.poll(0):
        # read from computer, send to pi
        ch = sys.stdin.read(1)
#        uart.write(ch.encode('utf-8'))
        uart.write(ch)
        
    if uart.any():
        # read from pi, send to computer
        s = uart.read()
        print(type(s), len(s))
        n = 0
        for c in s:
            print(n, chr(c))
            n += 1
#            print(c.decode('utf-8', end=''))
        
    # Small delay to avoid high CPU usage in the loop
    time.sleep(0.05)

