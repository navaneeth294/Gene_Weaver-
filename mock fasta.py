import random

def generate_mock_fasta(filename, length=50000, seed=42):
    random.seed(seed)  # same seed = same "random" sequence every time you run this
    bases = "ACGT"
    sequence = "".join(random.choice(bases) for _ in range(length))
    with open(filename, "w") as f:
        f.write(">mock_genome_50000bp\n")
        # real FASTA files wrap sequence lines at a fixed width (commonly 70 chars)
        for i in range(0, len(sequence), 70):
            f.write(sequence[i:i+70] + "\n")

generate_mock_fasta("mock_genome.fasta", length=50000)
print("Done — wrote mock_genome.fasta")
