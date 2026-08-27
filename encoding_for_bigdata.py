import time
import numpy as np
from numba import cuda
from Bio import SeqIO
from alignment_kernel import alignment_kernal

def encode_seq_fast(seq_str):
    seq_bytes = np.frombuffer(seq_str.encode('ascii'), dtype=np.uint8)
    lookup_table = np.zeros(256, dtype=np.uint8)
    lookup_table[ord('A')] = 0
    lookup_table[ord('C')] = 1
    lookup_table[ord('G')] = 2
    lookup_table[ord('T')] = 3
    return lookup_table[seq_bytes]

print("Reading 1-billion-letter genome file...")
record = next(SeqIO.parse("mock_genome_1b.fasta", "fasta"))
genome_str = str(record.seq)
guide_str = "GTTTG"


enc_genome = encode_seq_fast(genome_str)
enc_guide = encode_seq_fast(guide_str)

num_positions = len(enc_genome) - len(enc_guide) + 1
mismatch_counts = np.zeros(num_positions, dtype=np.uint8)

threads_per_block = 256
blocks = (num_positions + threads_per_block - 1) // threads_per_block

print(f"Positions to check: {num_positions:,}")


try:
    d_genome = cuda.to_device(enc_genome)
    d_guide = cuda.to_device(enc_guide)
    d_mismatch_counts = cuda.to_device(mismatch_counts)

    start = time.perf_counter()
    alignment_kernal[blocks, threads_per_block](d_genome, d_guide, d_mismatch_counts)
    cuda.synchronize()
    end = time.perf_counter()

    mismatch_counts = d_mismatch_counts.copy_to_host()
    matches = np.sum(mismatch_counts <= 1)

    print(f"SUCCESS — no memory error.")
    print(f"GPU found {matches} matches")
    print(f"GPU time taken: {end - start:.4f} seconds")

except cuda.cudadrv.driver.CudaAPIError as e:
    print(f"MEMORY ERROR: {e}")