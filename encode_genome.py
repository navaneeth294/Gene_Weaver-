import mock_fasta
import encode_seq
enc_genome = encode_seq(mock_fasta.mock_fasta.fasta)
enc_guide = encode_seq("GTTH")
print(len(enc_genome))
print(len(enc_guide))