from numba import cuda

@cuda.jit
def alignment_kernal(genome,guide,mismatch_counts):
    i = cuda.grid(1)
    if i < mismatch_counts.size:
        k = guide.size
        mismatches = 0
        for j in range(k):
            if genome[i+j] != guide[j]:
                mismatches = mismatches + 1
        mismatch_counts[i] = mismatches
