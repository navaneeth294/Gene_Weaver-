def count_mismatches(seq1, seq2):
    mismatches = 0
    for sequence1,sequence2 in zip(seq1,seq2):
        
        if sequence1 != sequence2:
            mismatches += 1
    return mismatches
print(count_mismatches("ACGTAC","ATGTGC"))