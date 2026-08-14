# FUNCTION TO COUNT THE MISMATCHES IN A SEQUENCE
def count_mismatches(seq1, seq2):
    mismatches = 0
    for sequence1,sequence2 in zip(seq1,seq2):
        
        if sequence1 != sequence2:
            mismatches += 1
    return mismatches
#print(count_mismatches("ACGTAC","ATGTGC"))


#function to find max_matcheble pair
def find_matches(genome,guide,max_mismatches):
    n = len(genome)
    k= len(guide)
    matche = []
    for i in range(n-k+1):
        matches = genome[i:i+k]
        mismatches = count_mismatches(matches,guide)
        if mismatches <= max_mismatches:
            matche.append((i,matches))
            
    
           
    return matche
       
genome = "ACGTACGTTTGCATGCAGGTTTG"
guide =  "GTTTG"
print(find_matches(genome, guide, max_mismatches=1))
