import numpy as np
import mock_fasta as mf
def encode_seq(seq):
    base_to_num = {"A":0, "C":1, "G":2, "T":3}
    result = []
    for letter in seq:
        result.append(base_to_num[letter])
    return np.array(result, dtype=np.uint8)

print(encode_seq(mf.mock_fasta.fasta))