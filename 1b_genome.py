import numpy as np

n = 1_000_000_000
letter_codes = np.array([65, 67, 71, 84], dtype=np.uint8) 
random_indices = np.random.randint(0, 4, size=n, dtype=np.uint8)
sequence_bytes = letter_codes[random_indices]

with open("mock_genome_1b.fasta", "wb") as f:
    f.write(b">mock_genome_1000000000bp\n")
    f.write(sequence_bytes.tobytes())
    f.write(b"\n")