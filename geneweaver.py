import numpy as np
from numba import cuda

@cuda.jit
def add_kernel(x, y, out):
    i = cuda.grid(1)
    if i < x.size:
        out[i] = x[i] + y[i]

n = 1000
x = np.arange(n, dtype=np.float32)
y = np.arange(n, dtype=np.float32)
out = np.zeros(n, dtype=np.float32)

threads_per_block = 128
blocks = (n + threads_per_block - 1) // threads_per_block
add_kernel[blocks, threads_per_block](x, y, out)

print("First 5 results:", out[:5])
print("Success!" if np.allclose(out, x + y) else "Mismatch!")