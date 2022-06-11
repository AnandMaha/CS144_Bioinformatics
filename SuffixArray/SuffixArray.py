## no libraries allowed

def suffixArray(t):
    """computes the suffix array of string t by sorting all suffixes of t"""
    ## YOUR CODE HERE
    # for loop 
    arr = []
    # add all suffixes to arr
    for i in range(len(t)):
        arr.append(t[i:])
    arr2 = sorted(arr) # maintain arr to do index matching later
    for i in range(len(t)):
        arr2[i] = arr.index(arr2[i])
    return arr2 # returns number array of positions of ordered suffixes

f = open("test.txt", "r")         # open the file
text = f.readline().strip()            # text is on the first line
s = suffixArray(text)                  

print(' '.join(map(str,s)))            # expected output for GCGTGCCTGGTCA$ is 13 12 11 5 1 6 4 0 8 9 2 10 3 7

# outFile = open('test.txt', "w")
# print(' '.join(map(str,s)), file = outFile)            # expected output for GCGTGCCTGGTCA$ is 13 12 11 5 1 6 4 0 8 9 2 10 3 7