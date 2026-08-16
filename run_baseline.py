import time
from Bio import SeqIO
from geneweaver import count_mismatches,find_matches

record = next(SeqIO.parse("mock_genome.fasta","fasta"))
genome = str(record.seq)
guide = "GTTTG"
start = time.perf_counter()
results = find_matches(genome,guide,max_mismatches = 1)
end = time.perf_counter()
print(f"found {len(results)} matches")
print(f"time taken{end - start:.4f} seconds")
