from Bio import SeqIO
from encode_seq import encode_seq  
import numpy as np

record = next(SeqIO.parse("mock_genome.fasta", "fasta"))
genome = str(record.seq)

enc_genome = encode_seq(genome)
enc_guide = encode_seq("GTTTG")   

print(len(enc_genome))
print(len(enc_guide))

num_positions = len(enc_genome) - len(enc_guide) + 1
mismatch_counts = np.zeros(num_positions,dtype = np.uint8)

print(num_positions)
print(mismatch_counts.shape)