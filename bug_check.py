import numpy as np
from numba import cuda
from Bio import SeqIO
from geneweaver import find_matches
from encode_seq import encode_seq
from alignment_kernel import alignment_kernal

record = next(SeqIO.parse("mock_genome.fasta", "fasta"))
full_genome = str(record.seq)
genome = full_genome[:10000]   # small slice, easy to inspect
guide = "GTTTG"
max_mismatches = 1

# CPU
cpu_results = find_matches(genome, guide, max_mismatches)
cpu_positions = set(i for i, m in cpu_results)

# GPU
enc_genome = encode_seq(genome)
enc_guide = encode_seq(guide)
num_positions = len(enc_genome) - len(enc_guide) + 1
mismatch_counts = np.zeros(num_positions, dtype=np.uint8)
threads_per_block = 256
blocks = (num_positions + threads_per_block - 1) // threads_per_block
alignment_kernal[blocks, threads_per_block](enc_genome, enc_guide, mismatch_counts)
cuda.synchronize()
gpu_positions = set(int(i) for i in np.where(mismatch_counts <= max_mismatches)[0])

print("CPU matches:", len(cpu_positions))
print("GPU matches:", len(gpu_positions))
print("In CPU but not GPU:", sorted(cpu_positions - gpu_positions)[:10])
print("In GPU but not CPU:", sorted(gpu_positions - cpu_positions)[:10])