from Bio import SeqIO
record = SeqIO.parse("mock_genome.fasta","fasta")
for record in SeqIO.parse("mock_genome.fasta","fasta"):
    print(record.id)
    print(len(record.seq))