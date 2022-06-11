## no libraries allowed except for numpy, itertools and biopython
## no Bio.pairwise2 allowed

from numpy import zeros, where, unravel_index, argmax, shape
from Bio.Align import substitution_matrices

def localAlignment(x, y, sub, indel):
    ''' Calculate local alignment values of sequences x and y using
        dynamic programming.  Returns the dynamic programming table and
        the matrix of traceback pointer (0,1,2,3) where 0: stop, 1: diagonal, 2: up, 3: left '''
    D = zeros((len(x)+1, len(y)+1), dtype=int) # numpy matrix for scores
    T = zeros((len(x)+1, len(y)+1), dtype=int) # numpy matrix for pointers (0: stop, 1: diagonal, 2: up, 3: left)
    # STRATEGY: Initialize first row and column
    # Now start (1,1) and go row by row
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            up = D[i-1,j] + indel
            left = D[i,j-1] + indel
            diagonal = D[i-1,j-1] + sub.get(x[i-1]).get(y[j-1])
            D[i,j] = max( 0 , up ,left , diagonal )
            #assign T[i,j] proper direction
            # (0: stop, 1: diagonal, 2: up, 3: left)
            if D[i,j] == diagonal: # up
                T[i,j] = 1 
            elif D[i,j] == up: # up
                T[i,j] = 2 
            elif D[i,j] == left: # left
                T[i,j] = 3 
    return D,T

def tracebackLocal(T, x, y, i, j):
    """ Trace back the alignment from position (i,j) in
        matrix T of traceback pointers for strings x and y.
        Returns an alignment string """
    align1, align2 = '', ''
    # (0: stop, 1: diagonal, 2: up, 3: left)
    while T[i,j] != 0: # keep going until stop reached
        if T[i,j] == 1: # diagonal
            align1 += x[i-1]
            align2 += y[j-1]
            i -= 1
            j -= 1
        elif T[i,j] == 2: # up
            align1 += x[i-1]
            align2 += "-"
            i -= 1
        elif T[i,j] == 3: # left
            align1 += "-"
            align2 += y[j-1]
            j -= 1
    return align1[::-1]+'\n'+align2[::-1] # reverse the strings

f = open("test.txt", "r")                                # open the file
match,mismatch,gap = map(int,f.readline().strip().split(' ')) # read the parameters
p1 = f.readline().strip()                                     # read the first string
p2 = f.readline().strip()                                     # read the second string

pam250 = substitution_matrices.load('PAM250') # possible matrices are ['BENNER22', 'BENNER6', 'BENNER74', 'BLOSUM45', 'BLOSUM50', 'BLOSUM62', 'BLOSUM80', 'BLOSUM90', 'DAYHOFF', 'FENG', 'GENETIC', 'GONNET1992', 'HOXD70', 'JOHNSON', 'JONES', 'LEVIN', 'MCLACHLAN', 'MDM78', 'NUC.4.4', 'PAM250', 'PAM30', 'PAM70', 'RAO', 'RISLER', 'SCHNEIDER', 'STR', 'TRANS']
# pam250 is a numpy matrix, here is how to access the substitution cost for (A,M)
# print(pam25.get('A').get('M'))

M,T = localAlignment(p1, p2, pam250, -5)      # compute the dynamic programming matrix and traceback pointers, -5 is the penalty for indel
(i,j) = unravel_index(argmax(M), M.shape)     # index of the max in the matrix using numpy

# The dynamic programming matrix for this input should be
#[[ 0  0  0  0  0  0  0  0]
# [ 0  0  0  0  0  4  0  0]
# [ 0  0  4  1  0  0  4  0]
# [ 0  1  0  4  3  0  1  1]
# [ 0  0  2  2  4  0  0  0]
# [ 0  0  0  0  0 10  5  0]
# [ 0  0  0  0  0  5  7 15]]
print(M)
print(M.max())                                # alignment score is the max in the matrix
print(tracebackLocal(T, p1, p2, i, j))        # print alignment

#outFile = open("test1.txt", "w")   
#print(M.max(), file = outFile)                                # alignment score is the max in the matrix
#print(tracebackLocal(T, p1, p2, i, j), file = outFile)        # print alignment