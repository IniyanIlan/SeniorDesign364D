import time
import board
import neopixel_spi as neopixel
from multiprocessing.resource_tracker import unregister
from multiprocessing import shared_memory
import numpy as np
import random

time.sleep(2)

NUM_PIXELS = 82
PIXEL_ORDER = neopixel.RGB
COLORS = (0xFF0000, 0x00FF00, 0x0000FF) # Red Green Blue
ColorBlue = (0x0000FF)
DELAY = 0.1

COLOR_RANGE_OCEAN = [0x2000FF, 0x5911FA, 0x7e1c4a, 0xe688e3, 0x480d48, 0xFF00FF]  # Various ocean-like blues
COLOR_RANGE_EXPLODE = [0x00ff00, 0x30ff00, 0xffff00, 0x30b500]
COLOR_PLAYER_RANGE = [
    0x00FF00, # Red
    0x30ff00, # Orange
    0x0000FF, # Blue
    0x0065FF, # Purple
    0xA5FF00, # Gold
    0x00ccdd # Pink
]

shm_LEDRequest_name = 'LEDRequest' 
existingLEDRequest = shared_memory.SharedMemory(name=shm_LEDRequest_name)
ledRequest = np.ndarray(3, dtype=np.int16, buffer=existingLEDRequest.buf)



spi = board.SPI()


# Ensure the SPI is properly locked and configured
while not spi.try_lock():
    pass  # Wait until the SPI bus is free

spi.configure(baudrate=8000000)  # Set baudrate to 8 MHz
spi.unlock()
    

pixels = neopixel.NeoPixel_SPI(
    spi, NUM_PIXELS, pixel_order=PIXEL_ORDER, auto_write=False, brightness=1.0
)

def random_color(color_range):
    """Select a random color from the given range."""
    return random.choice(color_range)

def initialize_pixels(num_pixels, color_range):
    """Initialize all pixels with random colors and brightness levels."""
    pixels_data = []
    for _ in range(num_pixels):
        color = random_color(color_range)
        brightness = random.uniform(0.1, 1.0)  # Start with a random brightness
        pixels_data.append({"color": color, "brightness": brightness, "direction": random.choice([-1, 1])})
    return pixels_data

def adjust_brightness(color, brightness):
    """Adjust the brightness of a given color."""
    r = int(((color >> 16) & 0xFF) * brightness)
    g = int(((color >> 8) & 0xFF) * brightness)
    b = int((color & 0xFF) * brightness)
    return (r << 16) | (g << 8) | b

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
            
def ripple(pixels_data, color_range, speed=0.01):
    """Simulate the ripple effect with dynamic brightness changes."""
    dimming = []
    brightening = []

    # Separate pixels into dimming and brightening lists
    for i, pixel in enumerate(pixels_data):
        if pixel["direction"] == -1:
            dimming.append(i)
        else:
            brightening.append(i)

    # Update dimming pixels
    for i in dimming:
        pixels_data[i]["brightness"] -= speed  # Decrease brightness
        if pixels_data[i]["brightness"] <= 0.0:
            pixels_data[i]["brightness"] = 0.0
            pixels_data[i]["color"] = random_color(color_range)  # Pick a new color
            pixels_data[i]["direction"] = 1  # Switch to brightening

    # Update brightening pixels
    for i in brightening:
        pixels_data[i]["brightness"] += speed  # Increase brightness
        if pixels_data[i]["brightness"] >= 1.0:
            pixels_data[i]["brightness"] = 1.0
            pixels_data[i]["direction"] = -1  # Switch to dimming

    # Apply the changes to the NeoPixels
    for i, pixel in enumerate(pixels_data):
        adjusted_color = adjust_brightness(pixel["color"], pixel["brightness"])
        pixels[i] = adjusted_color

    pixels.show()  # Send the data to the LEDs


BRIGHTNESS_LEVELS = [0.1, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0]  # Varying brightness levels


def turnLEDOff():
    pixels.fill(0)
    pixels.show()

if __name__ == "__main__":
    try:
# Initialize pixel data for ocean by default
        pixel_data = initialize_pixels(NUM_PIXELS, COLOR_RANGE_OCEAN)
        print("Starting LED Code...")
        while True:
            if ledRequest[0] == 0:  # Ripple
                ripple(pixel_data, COLOR_RANGE_OCEAN, speed=0.003)
            
            elif ledRequest[0] == 1:  # Explosion
                print("Exploding...")
                # Reinitialize pixels for explosion
                pixel_data = initialize_pixels(NUM_PIXELS, COLOR_RANGE_EXPLODE)
                timeout = time.time() + 5
                while time.time() < timeout:
                    ripple(pixel_data, COLOR_RANGE_EXPLODE, speed=0.05)
                ledRequest[0] = 0  # Reset to ripple
            
            #elif ledRequest[0] == 2  and ledRequest[1] != -1:  # Player
            elif ledRequest[2] == 1:
                print("Player effect...")
                time.sleep(0.001)
                timeout = time.time() + 5
                print(f"We have color {ledRequest[1]}")
                color_range = [COLOR_PLAYER_RANGE[ledRequest[1]]]  # Use player-specific color
                print(COLOR_PLAYER_RANGE[ledRequest[1]])
                #pixel_data = initialize_pixels(NUM_PIXELS, color_range)
                while time.time() < timeout:
                    ripple(pixel_data, color_range, speed=0.02)
                ledRequest[0] = 0  # Reset to ripple
                ledRequest[1] = -1
                ledRequest[2] = 0
            
            elif ledRequest[0] == 3:  # Off
                print("Turning LEDs off...")
                turnLEDOff()
                ledRequest[0] = 0  # Reset to ripple as default state
                          
                
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