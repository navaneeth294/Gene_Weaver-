from Bio import SeqIO
from encode_seq import encode_seq   # assuming that's the file/function name you saved it as

record = next(SeqIO.parse("mock_genome.fasta", "fasta"))
genome = str(record.seq)

enc_genome = encode_seq(genome)
enc_guide = encode_seq("GTTTG")   # note: fixed to the real guide — "GTTH" isn't valid, H isn't a DNA letter

print(len(enc_genome))
print(len(enc_guide))