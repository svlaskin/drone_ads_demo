import utime
import time
import picoexplorer as display
from machine import UART
from machine import Pin
import select

# display.set_audio_pin(1)

# # First set enable pin to low for the grove RF
# p0 = Pin(0, Pin.OUT) # EN
# p1 = Pin(1,Pin.OUT) # CON

t_wait=1./9600.

uart = UART(id=1,baudrate=9600, parity=None, stop=1, bits=8, rx=Pin(5), tx=Pin(4),txbuf=64)
poll=select.poll()
poll.register(uart, select.POLLIN)


# a = True
# while a==True:
#     p0.value(1)
#     p1.value(1)
#     utime.sleep(10.)
#     print("init done")
#     a=False
# 
# b=True
# while b==True:
#     p0.value(1)
#     p1.value(1)
#     utime.sleep(0.2)
#     b=False

# Initialise display with a bytearray display buffer
buf = bytearray(display.get_width() * display.get_height() * 2)
display.init(buf)
n_mess_total = 0


# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(0, 0, 0)
    display.clear()
    display.update()


while True:
    if display.is_pressed(display.BUTTON_A):              # if a button press is detected then...
        clear()                                           # clear to black
        display.set_pen(255, 255, 255)                    # change the pen colour
        display.text("Tx On. B to STDBY ", 10, 10, 240, 4)  # display some text on the screen
        display.update()                                  # update the display
        
        # Main code block for init here
        Tx=True # started setup
        
        while Tx:
            if display.is_pressed(display.BUTTON_B):
                Tx=False
            
            #uart.write(hex(123456789123456789))
            uart.write(hex(0x8D4840D6202CC371C32CE0576098))
            utime.sleep(0.5)
#             while uart.any():
#                 print(uart.read())
        
        utime.sleep(0.5)
        clear()                                           # clear to black
        display.set_pen(255, 255, 255)                    # change the pen colour
        display.text("B to continue", 10, 10, 240, 4)  # display some text on the screen
        display.update()
        
        
        utime.sleep(1)                                    # pause for a sec
        clear()                                           # clear to black again
        
        
        
    elif display.is_pressed(display.BUTTON_B):
        clear()
        display.set_pen(0, 255, 255)
        display.text("Button B pressed", 10, 10, 240, 4)
        display.update()
        utime.sleep(1)
        clear()
        
    elif display.is_pressed(display.BUTTON_X):
        clear()
        display.set_pen(255, 0, 255)
        display.text("Listen, X to STDBY", 10, 10, 240, 4)
        display.update()
        
        listen=True
        
        time_start=time.time()
        time_start2=time.time()
        n_mess_rec = 0
        rate_inter=0
        
        while listen:
            clear()
            display.set_pen(255, 0, 255)
            display.text("Rate: "+str(rate_inter), 10, 10, 240, 4)
            display.update()
            
            while uart.any():
                
                message=uart.read()
                print(message)
                time_elapsed=time.time()-time_start
                
#                 if str(message)==str(b'0b101111000110000101001110'):
#                     n_mess_rec+=1

                if str(message)==str(b'0x8d4840d6202cc371c32ce0576098'):
                    n_mess_rec+=1
                    n_mess_total+=1
#                     display.set_tone(300)

                
                if time_elapsed>5:
                    rate_inter = n_mess_rec/(time_elapsed)
                    clear()
                    display.set_pen(255, 0, 255)
#                     display.text("Rate: "+str(rate_inter) + "n_mess: " + str(n_mess_rec), 10, 10, 240, 4)
                    display.text(str(n_mess_total), 10, 10, 240, 4)
                    display.update()
                    n_mess_rec=0
                    time_start=time.time()
                    time_start2=time.time()
#                     display.set_tone(-1)
 
                    
                
                utime.sleep(0.1)
                if display.is_pressed(display.BUTTON_B):
                    listen=False
            while not uart.any():
                time_silent = time.time()-time_start2
                if time_silent>2:
                    clear()
                    display.set_pen(255, 0, 255)
                    display.text("No messages received", 10, 10, 240, 4)
                    display.update()
                    time_start2=time.time()
                    
  
    elif display.is_pressed(display.BUTTON_Y):
        clear()
        display.set_pen(255, 255, 0)
        display.text("Transmitting. A to quit", 10, 10, 240, 4)
        display.update()
        
        transmit=True
        while transmit:
            print("transmit. A to quit")
            p0.value(1)
            p1.value(1)
            uart.write(1234)
            if display.is_pressed(display.BUTTON_A):
                transmit=False
            utime.sleep(0.5)
            
        utime.sleep(1)
        clear()
    else:
        display.set_pen(255, 0, 0)
        display.text("Standby. A to Tx, X to Rx", 10, 10, 240, 4)
        display.update()
    utime.sleep(0.1)  # this number is how frequently the Pico checks for button presses
    













