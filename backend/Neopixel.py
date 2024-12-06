import time
import board
import neopixel_spi as neopixel
from multiprocessing.resource_tracker import unregister
from multiprocessing import shared_memory
import numpy as np

NUM_PIXELS = 82
PIXEL_ORDER = neopixel.RGB
COLORS = (0xFF0000, 0x00FF00, 0x0000FF) # Green Red Blue
ColorBlue = (0x0000FF)
DELAY = 0.1

shm_LEDRequest_name = 'LEDRequest' 
existingLEDRequest = shared_memory.SharedMemory(name=shm_LEDRequest_name)
ledRequest = np.ndarray(2, dtype=np.int16, buffer=existingLEDRequest.buf)



spi = board.SPI()


# Ensure the SPI is properly locked and configured
while not spi.try_lock():
    pass  # Wait until the SPI bus is free

spi.configure(baudrate=8000000)  # Set baudrate to 8 MHz
spi.unlock()
    

pixels = neopixel.NeoPixel_SPI(
    spi, NUM_PIXELS, pixel_order=PIXEL_ORDER, auto_write=False, brightness=1.0
)



def breathe():
    breatheUp = 0
    timeout = time.time() + 5
    while timeout < 5:
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

def turnLEDOff():
    pixels.fill(0)
    pixels.show()

if __name__ == "__main__":
    try:
        while True:
            if(ledRequest[0] == 0):
                breathe()
            elif(ledRequest[0] == 4):
                turnLEDOff()
            

            
                
                
                
                # for i in range(NUM_PIXELS):
                #     pixels[i] = color
                #     pixels.show()
                #     #time.sleep(DELAY)
                #     pixels.fill(0)
    except(KeyboardInterrupt):
        print("Exiting and cleaning up...")
        
        # Reset NeoPixel or any devices using SPI
        pixels.deinit()  # Deinitialize the NeoPixel object
        
        # Ensure the SPI pins are released
        while not spi.try_lock():
            pass
        spi.configure(baudrate=0)  # Reset SPI configuration
        spi.unlock()
        pass