import numpy as np
from multiprocessing import shared_memory
from multiprocessing.resource_tracker import unregister
from multiprocessing.managers import SharedMemoryManager
import subprocess
import time

# Create a NumPy array with some initial data
data = np.array([6, 3, 3, 4, 5], dtype=np.int64)
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


# Unregister the shared memory block from the resource_tracker
#unregister(shm._name, 'shared_memory')
#unregister(shm_int._name, 'shared_memory')

# Copy data into shared memory
shared_array[:] = data[:]

print(f"Shared memory name: {shm.name}")
print(f"Data in shared memory: {shared_array}")
print(f"Shared memory name: {shm_int.name}")
print(f"Data in shared memory: {sharedInt}")

# Unregister the memory blocks from the resource tracker. Its cringe
#unregister(shm._name, 'shared_memory')
#unregister(shm_int._name, 'shared_memory')

# Run Peripheral program from master program using subprocess, passing the shared memory name
process = subprocess.Popen(['python3', 'PeripheralFileMultiprocessing.py', shm.name, shm_int.name])



# After Peripheral program runs, check the modified data
print(f"Data in shared array after Peripheral program: {shared_array}")
print(f"Data in shared integer after Peripheral program: {sharedInt}")

n = 0
while(sharedInt[0] != 52):
    time.sleep(0.1)


print(f"Integer was changed to {sharedInt[0]}!")

time.sleep(1)
process.wait()


print(f"Name of shared mem1: {shm.name}")
print(f"Name of shared mem2: {shm_int.name}")


#time.sleep(10)
# Clean up shared memory HAVE TO RELEASE, DUH
shm.close()
shm_int.close()



shm.unlink()
shm_int.unlink()

time.sleep(5)