import RPi.GPIO as GPIO
import time


matrix = [[0] * 5 for i in range(8)]

#Pins for easy debugging
PIN8 = 14
PIN10 = 15
PIN12 = 18

PIN3 = 2
PIN5 = 3
PIN7 = 4
PIN11 = 17
PIN13 = 27

def matrixInit():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Set up selector bits for MUXes (Pins 8, 10, 12) (GPIO 14, 15, 18)
    GPIO.setup(PIN8, GPIO.OUT, initial=0) # selector 1 (LSB)
    GPIO.setup(PIN10, GPIO.OUT, initial=0) # Selector 2
    GPIO.setup(PIN12, GPIO.OUT, initial=0) # Selector 3 (MSB)

    #Set MUX Output GPIOs (3,5,7,11,13) OR (2, 3, 4, 17, 27)
    # SET HERE WHEN THE PCB GETS HERE PLS

    GPIO.setup(2, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(3, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(4, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(17, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(27, GPIO.IN, GPIO.PUD_DOWN)

    #Set MUX Output GPIOs (3,5,7,9,11)
    # SET HERE WHEN THE PCB GETS HERE PLS

def countRow(row):
    # Set selector row
    match row:
        case 0:
            GPIO.output(PIN12, 0)
            GPIO.output(PIN10, 0)
            GPIO.output(PIN8,  0)
        case 1:
            GPIO.output(PIN12, 0)
            GPIO.output(PIN10, 0)
            GPIO.output(PIN8,  1)
        case 2:
            GPIO.output(PIN12, 0)
            GPIO.output(PIN10, 1)
            GPIO.output(PIN8,  0)
        case 3:
            GPIO.output(PIN12, 0)
            GPIO.output(PIN10, 1)
            GPIO.output(PIN8,  1)
        case 4:
            GPIO.output(PIN12, 1)
            GPIO.output(PIN10, 0)
            GPIO.output(PIN8,  0)
        case 5:
            GPIO.output(PIN12, 1)
            GPIO.output(PIN10, 0)
            GPIO.output(PIN8,  1)
        case 6:
            GPIO.output(PIN12, 1)
            GPIO.output(PIN10, 1)
            GPIO.output(PIN8,  0)
        case 7:
            GPIO.output(PIN12, 1)
            GPIO.output(PIN10, 1)
            GPIO.output(PIN8,  1)
    time.sleep(0.01) # might need to wait a second since the propagation of the MUX might be slower than the clock speed
    matrix[row][0] = GPIO.input(PIN3)
    time.sleep(0.01)
    matrix[row][1] = GPIO.input(PIN5)
    time.sleep(0.01)
    matrix[row][2] = GPIO.input(PIN7)
    time.sleep(0.01)
    matrix[row][3] = GPIO.input(PIN11)
    time.sleep(0.01)
    matrix[row][4] = GPIO.input(PIN13)



    
    # global rowCount
    # if (rowCount == 0):
    #     presentMatrix[0][0] = 1 - GPIO.input(3)
    #     presentMatrix[0][1] = 1 - GPIO.input(5)
    # elif (rowCount == 1):
    #     presentMatrix[1][0] = 1 - GPIO.input(7)
    #     presentMatrix[1][1] = 1 - GPIO.input(11)
    # rowCount += 1
    return


def scanMatrix():
    for i in range(8):
        countRow(i)



    
    # global rowCount
    # if (rowCount == 0):
    #     presentMatrix[0][0] = 1 - GPIO.input(3)
    #     presentMatrix[0][1] = 1 - GPIO.input(5)
    # elif (rowCount == 1):
    #     presentMatrix[1][0] = 1 - GPIO.input(7)
    #     presentMatrix[1][1] = 1 - GPIO.input(11)
    # rowCount += 1
    return


def scanMatrix():
    for i in range(8):
        countRow(i)


if __name__ == "__main__":
    matrixInit()
    while True:
        if input("Scan the board? (y/n)") == "y":  # Call input() directly, don't assign
            scanMatrix()
            print(matrix)
            #GPIO.output([12, 10, 8], [GPIO.LOW, GPIO.LOW, GPIO.LOW]) # 000
        elif input("Scan the board? (y/n)") == "n":  # Handle "n" input for loop exit
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
    