## no libraries allowed except for numpy and biopython 
## no Bio.pairwise2 allowed

from numpy import zeros

def globalAlignment(x, y, match, mismatch, gap):
    """ Calculate the global alignment between sequences x and y using
        dynamic programming using <match> reward, a <mismatch> penalty, an <gap> penalty
        Return the full dynamic programming table. """
    D = zeros((len(x)+1, len(y)+1), dtype=int) # initialize a numpy matrix with zeroes
    # STRATEGY: Initialize first row and column
    for i in range(len(x)+1):
        D[i,0] = D[i-1,0] - gap if i != 0 else 0
    for i in range(len(y)+1):
        D[0,i] = D[0,i-1] - gap if i != 0 else 0
    # Now start (1,1) and go row by row
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            temp = D[i-1,j-1] - mismatch
            if x[i-1] == y[j-1]:
                temp = D[i-1,j-1] + match
            D[i,j] = max( D[i-1,j] - gap , D[i,j-1] - gap , temp )
    return D

def tracebackGlobal(V, x, y, match, mismatch, gap):
    """ Trace back the alignment from position (len(x), len(y)) in global alignment matrix V """
    align1, align2 = '', ''
    i, j = len(x),len(y) # start from the bottom right cell
    # STRATEGY: from bottom right, travel to highest score in adj. top left, end top left
    while i > 0 or j > 0:
        
        # solve direction to move
        dir = 0 # 0 to move left, 1 to move up-left, 2 to move up
        currVal = V[i,j]
        temp = -1 * mismatch
        if x[i-1] == y[j-1]:
            temp = match
        if currVal == V[i-1,j-1] + temp : # move up-left
            dir = 1
        elif currVal == V[i-1,j] - gap: # move up
            dir = 2
        if i == 0: # first row, must go left
            dir = 0
        elif j == 0: # first col, must go up
            dir = 2

        # add appropriate symbols to allign 1 and 2
        if dir == 1: # up-left
            align1 += x[i-1]
            align2 += y[j-1]
            i -= 1
            j -= 1
        elif dir == 0: # left
            align1 += "-"
            align2 += y[j-1]
            j -= 1
        elif dir == 2: # up
            align1 += x[i-1]
            align2 += "-"
            i -= 1
    return align1[::-1]+'\n'+align2[::-1]  # reverse the strings

f = open("test.txt", "r")                                # open the file
match,mismatch,gap = map(int,f.readline().strip().split(' ')) # read the parameters
p1 = f.readline().strip()                                     # read the first string
p2 = f.readline().strip()                                     # read the second string

M = globalAlignment(p1, p2, match, mismatch, gap)         # compute the dynamic programming matrix betwen p1 and p2, using match, sub, indel penalties
# The dynamic programming matrix for this input should be
# [[ 0 -2 -4 -6]
# [-2  1 -1 -3]
# [-4 -1  2  0]
# [-6 -3  0  1]
# [-8 -5 -2 -1]]

print(M[len(p1),len(p2)])                                 # alignment score in on lower right corner cell
print(tracebackGlobal(M, p1, p2, match, mismatch, gap))   # print alignment

# outFile = open("test1.txt", "w") 
# print(M[len(p1),len(p2)], file = outFile)                                 # alignment score in on lower right corner cell
# print(tracebackGlobal(M, p1, p2, match, mismatch, gap), file = outFile)   # print alignment