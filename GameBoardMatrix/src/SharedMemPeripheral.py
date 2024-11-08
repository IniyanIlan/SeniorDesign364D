from multiprocessing.resource_tracker import unregister
from multiprocessing import shared_memory
import numpy as np
import time
import subprocess


# Access the shared memory by name
shm_name = 'Matrix'  # Replace with actual shm.name from main process
array_shape = (5, 8)  # Same shape as created initially
array_dtype = np.int8  # Same dtype as initially created

# Connect to the existing shared memory block
existing_shmMatrix = shared_memory.SharedMemory(name='Matrix')

# Create a 2D NumPy array using the existing shared memory
shared_array = np.ndarray(array_shape, dtype=array_dtype, buffer=existing_shmMatrix.buf)

print(shared_array)

existing_shmMatrix.close()
#unregister(existing_shmMatrix._name, 'shared_memory')