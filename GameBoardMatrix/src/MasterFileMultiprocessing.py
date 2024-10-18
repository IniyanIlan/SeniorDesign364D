import numpy as np
from multiprocessing import shared_memory
import subprocess

# Create a NumPy array with some initial data
data = np.array([1, 2, 3, 4, 5], dtype=np.int64)
# Declare an array of size one with int 32 type memory usage.
num = np.array([42], dtype=np.int32)
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
subprocess.run(['python3', 'PeripheralFileMultiprocessing.py', shm.name, shm_int.name])

# After Peripheral program runs, check the modified data
print(f"Data in shared array after Peripheral program: {shared_array}")
print(f"Data in shared integer after Peripheral program: {sharedInt}")


# Clean up shared memory
shm.close()
shm.unlink()