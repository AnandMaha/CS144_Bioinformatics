## no libraries allowed

def bwt(t):
    '''computes the BWT(t), where t is a string'''
    ## YOUR CODE HERE
    #make the burrows wheeler matrix from t
    bw_matrix = []
    for i in range(len(t)):
        strt = -len(t) + i
        end = i
        bw_matrix.append(t[strt:] + t[:end])
    bw_matrix.sort()
    # return last character of strings concatenated
    bwt_text = ""
    for s in bw_matrix:
        bwt_text += s[len(s)-1]
    return bwt_text

f = open("test.txt", "r")         # open the file
text = f.readline().strip()            # text is on the first line

print(bwt(text))                       # expected output ACTGGCT$TGCGGC
# outFile = open("test.txt", "w")
# print(bwt(text), file = outFile)                       # expected output ACTGGCT$TGCGGC
