import time
import board
import neopixel_spi as neopixel

NUM_PIXELS = 82
PIXEL_ORDER = neopixel.RGB
COLORS = (0xFF0000, 0x00FF00, 0x0000FF) # Green Red Blue
ColorBlue = (0x0000FF)
DELAY = 0.1


spi = board.SPI()


# Ensure the SPI is properly locked and configured
while not spi.try_lock():
    pass  # Wait until the SPI bus is free

spi.configure(baudrate=8000000)  # Set baudrate to 8 MHz
spi.unlock()
    

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
        
        
        
        # for i in range(NUM_PIXELS):
        #     pixels[i] = color
        #     pixels.show()
        #     #time.sleep(DELAY)
        #     pixels.fill(0)