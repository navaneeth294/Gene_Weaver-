import time
from Bio import SeqIO
from geneweaver import find_matches

print("Reading 1-billion-letter genome...")
record = next(SeqIO.parse("mock_genome_1b.fasta", "fasta"))
genome = str(record.seq)
guide = "GTTTG"

print("Running CPU search")
start = time.perf_counter()
results = find_matches(genome, guide, max_mismatches=1)
end = time.perf_counter()

print(f"CPU found {len(results)} matches")
print(f"CPU time taken: {end - start:.4f} seconds")