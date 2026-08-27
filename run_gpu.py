import time
import numpy as np
from Bio import SeqIO
from encode_seq import encode_seq
from numba import cuda
from alignment_kernel import alignment_kernal


record = next(SeqIO.parse("mock_genome.fasta","fasta"))
genome_str = str(record.seq)
guide_str = "GTTTG"

encode_genome = encode_seq(genome_str)
encode_guide = encode_seq(guide_str)


num_positions = len(encode_genome) - len(encode_guide) + 1
mismatch_counts = np.zeros(num_positions, dtype = np.uint8)


threads_perblock = 256
blocks = (num_positions + threads_perblock - 1) // threads_perblock


d_genome = cuda.to_device(encode_genome)
d_guide = cuda.to_device(encode_guide)
d_mismatch_counts = cuda.to_device(mismatch_counts)




start = time.perf_counter()
alignment_kernal[blocks, threads_perblock](d_genome,d_guide,d_mismatch_counts)
cuda.synchronize()
end = time.perf_counter()

mismatch_counts = d_mismatch_counts.copy_to_host()
max_mismatches = 1
matches = np.sum(mismatch_counts <= max_mismatches)

print(f"GPU Found {matches} Matches")
print(f"time taken for gpu to find matches {end - start:.4f} seconds")