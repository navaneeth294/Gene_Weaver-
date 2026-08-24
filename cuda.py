@cuda.jit
def alignment_kernal(genome,guide,mismatch_counts):
    i = cuda.grid(1)
    if i < mismatch_count.size:
        pass
