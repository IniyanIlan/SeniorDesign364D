import RPi.GPIO as GPIO
import time


matrix = [[0] * 5 for i in range(8)]

def matrixInit():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    # Set up selector bits for MUXes (Pins 8, 10, 12)
    GPIO.setup(8, direction=GPIO.OUT, initial=GPIO.LOW) # selector 1 (LSB)
    GPIO.setup(10, direction=GPIO.OUT, initial=GPIO.LOW) # Selector 2
    GPIO.setup(12, direction=GPIO.OUT, initial=GPIO.LOW) # Selector 3 (MSB)

    #Set MUX Output GPIOs (3,5,7,9,11)
    # SET HERE WHEN THE PCB GETS HERE PLS

    GPIO.setup(3, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(5, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(7, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(11, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(13, GPIO.IN, GPIO.PUD_DOWN)


def countRow(row):
    # Set selector row
    match row:
        case 0:
            GPIO.output([12, 10, 8], [GPIO.LOW, GPIO.LOW, GPIO.LOW]) # 000
        case 1:
            GPIO.output([12, 10, 8], [GPIO.LOW, GPIO.LOW, GPIO.HIGH]) # 001
        case 2:
            GPIO.output([12, 10, 8], [GPIO.LOW, GPIO.HIGH, GPIO.LOW]) # 010
        case 3:
            GPIO.output([12, 10, 8], [GPIO.LOW, GPIO.HIGH, GPIO.HIGH]) # 011
        case 4:
            GPIO.output([12, 10, 8], [GPIO.HIGH, GPIO.LOW, GPIO.LOW]) # 100
        case 5:
            GPIO.output([12, 10, 8], [GPIO.HIGH, GPIO.LOW, GPIO.HIGH]) # 101
        case 6:
            GPIO.output([12, 10, 8], [GPIO.HIGH, GPIO.HIGH, GPIO.LOW]) # 110
        case 7:
            GPIO.output([12, 10, 8], [GPIO.HIGH, GPIO.HIGH, GPIO.HIGH]) # 111
    #time.sleep(0.1) # might need to wait a second since the propagation of the MUX might be slower than the clock speed
    matrix[row][0] = GPIO.input(3)
    matrix[row][1] = GPIO.input(5)
    matrix[row][2] = GPIO.input(7)
    matrix[row][3] = GPIO.input(11)
    matrix[row][4] = GPIO.input(13)



    
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
            GPIO.output([12, 10, 8], [GPIO.LOW, GPIO.LOW, GPIO.LOW]) # 000
        elif input("Scan the board? (y/n)") == "n":  # Handle "n" input for loop exit
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
    