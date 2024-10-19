# program2.py
import sys
import numpy as np
from multiprocessing import shared_memory
import time

# Read shared memory name from command-line argument
shm_name = sys.argv[1]
shm_int_name = sys.argv[2]

# Access the existing shared memory block by name
existing_shm = shared_memory.SharedMemory(name=shm_name)
sharedInt_shm = shared_memory.SharedMemory(name=shm_int_name)

# Create a NumPy array backed by the existing shared memory
shared_array = np.ndarray((5,), dtype=np.int64, buffer=existing_shm.buf)
sharedInt = np.ndarray((1,), dtype=np.int32, buffer=sharedInt_shm.buf)


print(f"Data in shared memory before modification: {shared_array}")
print(f"Data in shared memory before modification: {sharedInt}")

# Modify the shared array
shared_array[0] = 100
sharedInt[0] = sharedInt[0] + 1000
print(f"Data in shared memory after modification: {shared_array}")
print(f"Data in shared memory after modification: {sharedInt}")
n = 0
time.sleep(5)

sharedInt[0] = 52
    
print(f"name of first shared memory {existing_shm.name}")
print(f"name of second shared memory {sharedInt_shm.name}")

#time.sleep(10)

# Close the shared memory block (no need to unlink since Program 1 owns it)
existing_shm.close()
sharedInt_shm.close()
#existing_shm.unlink()
#sharedInt_shm.unlink()

time.sleep(5)
