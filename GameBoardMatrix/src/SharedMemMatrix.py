from multiprocessing.resource_tracker import unregister
from multiprocessing import shared_memory
import numpy as np
import time
import subprocess




# Hall effect Matrix Init

# Define the shape and data type of your 2D array
array_shape = (5, 8)  # For example, a 5x5 array
array_dtype = np.int8  # Specify the data type

# Array Size
nbytes = int(np.prod(array_shape) * np.dtype(array_dtype).itemsize)

# Create the shared memory block
shmMatrix = shared_memory.SharedMemory(create=True, size=nbytes, name='Matrix')

# Create a 2D NumPy array backed by the shared memory
shared_array = np.ndarray(array_shape, dtype=array_dtype, buffer=shmMatrix.buf)

# Initialize the array with some values
shared_array[:] = 1
time.sleep(.5)
process = subprocess.Popen(['python3 ', 'C:\SeniorDesign\SeniorDesign364D\GameBoardMatrix\src\SharedMemPeripheral.py'])


print(shmMatrix.name)
print(shared_array)

time.sleep(.5)

shmMatrix.close()
shmMatrix.unlink()