import time
import board
import random
import neopixel_spi as neopixel

NUM_PIXELS = 82
PIXEL_ORDER = neopixel.RGB
COLORS = (0xFF0000, 0x00FF00, 0x0000FF)  # Green, Red, Blue
DELAY = 0.01  # Smooth breathing effect delay

spi = board.SPI()

# Ensure the SPI is properly locked and configured
while not spi.try_lock():
    pass
spi.configure(baudrate=8000000)
spi.unlock()

pixels = neopixel.NeoPixel_SPI(
    spi, NUM_PIXELS, pixel_order=PIXEL_ORDER, auto_write=False, brightness=1.0
)

COLOR_RANGE_OCEAN = [0x2000FF, 0x5911FA, 0x7e1c4a, 0xe688e3, 0x480d48, 0xFF00FF]  # Various ocean-like blues
COLOR_RANGE_EXPLODE = [0x00ff00, 0x30ff00, 0xffff00, 0x30b500]

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


# light up pixels in chunks
# 3 cycles is base
def breathe(pixelIndexLeft, pixelIndexRight, color, cycles=3):
    """Create a breathing effect for a specific pixel."""
    for _ in range(cycles):
            # Fade in
        for brightness in [x / 500 for x in range(501)]:
            for pixel_index in range(pixelIndexLeft, pixelIndexRight):
                pixels[pixel_index] = adjust_brightness(color, brightness)
            pixels.show()
            #time.sleep(DELAY)

            # Fade out
        for brightness in [x / 500 for x in range(500, -1, -1)]:
            for pixel_index in range(pixelIndexLeft, pixelIndexRight):
                pixels[pixel_index] = adjust_brightness(color, brightness)
            pixels.show()
            #time.sleep(DELAY)

def raceDown(colors, brightness_levels, delay=0.05):
    """
    Create a ripple effect using a range of colors and brightness levels.
    
    Args:
        colors: List of colors to use in the ripple.
        brightness_levels: List of brightness levels to vary the effect.
        delay: Time delay between ripple updates.
    """
    for i in range(NUM_PIXELS):
        # Choose a random color and brightness for the ripple
        color = random.choice(colors)
        brightness = random.choice(brightness_levels)
        
        # Adjust the color brightness
        adjusted_color = adjust_brightness(color, brightness)
        
        # Apply the ripple effect
        pixels.fill(0)  # Reset all pixels to off
        pixels[i] = adjusted_color  # Light up the current pixel
        pixels.show()
        time.sleep(delay)

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

if __name__ == "__main__":
        # Example: Breathe effect for pixel 10 with red color
    #breathe(pixelIndexLeft=0, pixelIndexRight=NUM_PIXELS, color=0x004b88)
    pixels_data = initialize_pixels(NUM_PIXELS, COLOR_RANGE_EXPLODE)
    # Potential defuse mode
    #raceDown([0x00ff00, 0x30ff00, 0xffff00, 0x50a500], BRIGHTNESS_LEVELS, 0.3)
    try:
        while True:
            #ripple(pixels_data, COLOR_RANGE_OCEAN, 0.003)
            ripple(pixels_data, COLOR_RANGE_EXPLODE, 0.05)
            #time.sleep(DELAY)

        # Reset pixels
            pixels.fill(0)
            pixels.show()
    except KeyboardInterrupt:
        # Clean up on exit
        pixels.fill(0)
        pixels.show()
