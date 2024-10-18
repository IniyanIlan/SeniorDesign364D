import numpy as np
from multiprocessing import shared_memory
import subprocess
import time

# Create a NumPy array with some initial data
data = np.array([6, 3, 3, 4, 5, 10], dtype=np.int64)
# Declare an array of size one with int 32 type memory usage.
num = np.array([0], dtype=np.int32)
# Create a shared memory block
shm = shared_memory.SharedMemory(create=True, size=data.nbytes)

# create a num memory block (4 bytes, 32bit int)
shm_int = shared_memory.SharedMemory(create=True, size=num.nbytes)

sharedInt = np.ndarray(num.shape, dtype=num.dtype, buffer=shm_int.buf)

# Create a NumPy array backed by the shared memory
shared_array = np.ndarray(data.shape, dtype=data.dtype, buffer=shm.buf)

sharedInt[:] = num[:]

# Copy data into shared memory
shared_array[:] = data[:]

print(f"Shared memory name: {shm.name}")
print(f"Data in shared memory: {shared_array}")
print(f"Shared memory name: {shm_int.name}")
print(f"Data in shared memory: {sharedInt}")

# Run Peripheral program from master program using subprocess, passing the shared memory name
process = subprocess.Popen(['python', 'PeripheralFileMultiprocessing.py', shm.name, shm_int.name])



# After Peripheral program runs, check the modified data
print(f"Data in shared array after Peripheral program: {shared_array}")
print(f"Data in shared integer after Peripheral program: {sharedInt}")

n = 0
while(sharedInt[0] != 52):
    time.sleep(0.1)


print(f"Integer was changed to {sharedInt[0]}!")

process.wait()


# Clean up shared memory HAVE TO RELEASE, DUH
shm.close()
shm.unlink()
shm_int.close()
shm_int.unlink()