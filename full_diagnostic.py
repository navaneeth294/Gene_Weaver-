import numpy as np
from numba import cuda
from Bio import SeqIO
from geneweaver import find_matches
from encode_seq import encode_seq
from alignment_kernel import alignment_kernal

record = next(SeqIO.parse("mock_genome.fasta", "fasta"))
genome = str(record.seq)
guide = "GTTTG"
max_mismatches = 1

print("Running CPU (this takes ~12 seconds, be patient)...")
cpu_results = find_matches(genome, guide, max_mismatches)
cpu_positions = set(i for i, m in cpu_results)

print("Running GPU...")
enc_genome = encode_seq(genome)
enc_guide = encode_seq(guide)
num_positions = len(enc_genome) - len(enc_guide) + 1
mismatch_counts = np.zeros(num_positions, dtype=np.uint8)
threads_per_block = 256
blocks = (num_positions + threads_per_block - 1) // threads_per_block

d_genome = cuda.to_device(enc_genome)
d_guide = cuda.to_device(enc_guide)
d_mismatch_counts = cuda.to_device(mismatch_counts)
alignment_kernal[blocks, threads_per_block](d_genome, d_guide, d_mismatch_counts)
cuda.synchronize()
mismatch_counts = d_mismatch_counts.copy_to_host()

gpu_positions = set(int(i) for i in np.where(mismatch_counts <= max_mismatches)[0])

extra = sorted(gpu_positions - cpu_positions)
missing = sorted(cpu_positions - gpu_positions)

print("CPU matches:", len(cpu_positions))
print("GPU matches:", len(gpu_positions))
print("Total positions:", num_positions)
print("Extra in GPU, not in CPU (first 15):", extra[:15])
print("Missing from GPU, present in CPU (first 15):", missing[:15])
print("mismatch_count values at those extra positions:", [int(mismatch_counts[p]) for p in extra[:15]])
print("Do extras cluster near the end? last extra position:", extra[-1] if extra else "none")