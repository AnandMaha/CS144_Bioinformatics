## no libraries allowed

def reverseBwt(t):
    '''computes the inverse of the BWT, where t is a string'''
    # go through t and assign value to letters based on num of appearances
    bwt_lst_col = []
    for i in range(len(t)):
        temp = (t[i], t[:i+1].count(t[i]))
        bwt_lst_col.append(temp)
    bwt_frst_col = sorted(bwt_lst_col, key = lambda x: x[0]) # sort lexicographically to get first
    # start from $ in frst_col to build orginal string backwards
    str = ""
    idx = 0 # $ always 0th element in frst_col
    for i in range(len(t)):
        str = bwt_frst_col[idx][0] + str # build str backwards
        idx = bwt_frst_col.index(bwt_lst_col[idx]) # find exact match in frst_col from last
    return str

f = open("test.txt", "r")         # open the file
text = f.readline().strip()            # text is on the first line
print(reverseBwt(text))                # expected output TACATCACGT$
# outFile = open("test.txt", "w") 
# print(reverseBwt(text), file = outFile)                # expected output TACATCACGT$