import RPi.GPIO as GPIO
import time
import time
import board
import neopixel_spi as neopixel
import busio

NUM_PIXELS = 82
PIXEL_ORDER = neopixel.RGB
COLORS = (0xFF0000, 0x00FF00, 0x0000FF) # Green Red Blue
ColorBlue = (0x0000FF)
DELAY = 0.1


spi = board.SPI()
if(GPIO.getmode() == GPIO.BCM):
    print(GPIO.getmode())

# Simple program made to test GPIO pin usage on the RPI 5.
# Pressing the button 4 times will end the program.

GPIO.setup(14,GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(15, GPIO.IN, GPIO.PUD_DOWN)
n = 0
flag = True
pixels = neopixel.NeoPixel_SPI(
    spi, NUM_PIXELS, pixel_order=PIXEL_ORDER, auto_write=False, brightness=1.0
)

breatheUp = 0


while True:
    for color in COLORS:
        while(breatheUp != ColorBlue):
            pixels.fill(breatheUp + 1)
            #[pixels [i] for i in range(NUM_PIXELS)] = breatheUp + 1
            breatheUp += 1
            pixels.show()
            #time.sleep(0.001)
        while(breatheUp != 0):
            pixels.fill(breatheUp - 1)
            #[pixels [i] for i in range(NUM_PIXELS)] = breatheUp + 1
            breatheUp -= 1
            pixels.show()
            #time.sleep(0.001)
        