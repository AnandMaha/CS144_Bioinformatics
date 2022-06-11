import random

def score_profile(s, p):
    """ computes the probability of string s using the profile p """
    prob = p[0][s[0]]
    for i in range(1, len(s)):
        prob *= p[i][s[i]]
    return prob

def profile_pseudo(S):
    """ Given a vector of strings S of the same length computes the matrix profile of S, i.e.,
        the probability of As, Cs, Gs and Ts in each column, including a pseudo-count of 1; each
        column is scaled by the number of strings + 4, so that the probabilities in each column sum up to one"""
    p = []
    n = len(S[0])
    # we are adding one additional occurrence (pseudo-count)
    # of A, C, G and T to the columns, so the total # of symbols
    # column-wise is t = len(S) + 4
    t = len(S) + 4
    # compute probability distribution column by column
    for i in range(n):
        p.append({'A': 1.0/t, 'T': 1.0/t, 'C': 1.0/t, 'G': 1.0/t}) # pseudo-count of 1
        for s in S:
            p[i][s[i]] += (1.0 / t)
    return p

def count(S):
    """ Given a vector S of strings of the same length computes the count profile of S, i.e.,
        counts of As, Cs, Gs and Ts in each column """
    p = []
    n = len(S[0])
    # compute counts column by column
    for i in range(n):
        p.append({'A': 0.0, 'T': 0.0, 'C': 0.0, 'G': 0.0})
        for s in S:
            p[i][s[i]] += 1.0
    return p

def GibbsSampler(S, k, t, N):
    """ find the best motifs of length k using Gibbs sampling from a set S of t strings,
        by running N iterations """
    # n is the length of the input strings
    n = len(S[0])

    # best is the best set of k-mers we found so far, best[0] contains the score
    # and best[1] the vector of k-mers
    best = (0,[])
    
    # m is the current set of k-mers
    m = []
    
    # randomly select k-mers from each of the string in S
    for i in range(t):
        j = random.randrange(n-k+1)
        m.append(S[i][j:j+k])       

    # run N iterations of sampling
    for _ in range(N):
        # 1. score the k-mers in m by computing the sum of the frequencies of the most
        #    frequent symbol in the current profile m (use the function count() to obtain the counts)
        counts = count(m)
        score = 0
        for i in range(len(counts)):
            temp_max = -1
            for l in counts[i]:
                if counts[i][l] > temp_max:
                    temp_max =  counts[i][l]
            score += temp_max
            
        # 2. remember the best set of k-mers
        if best[0] < score:
            best = (score,list(m))
            
        # 3. select a string i at random that need to be ignored (random number in [0...t-1])
        i = random.randrange(t)

        # 4. build the profile excluding the i-th string using pseudo counts
        #    (call profile_pseudo() of the vector m excluding the i-th k-mer)
        p = profile_pseudo([m[j] for j in range(len(m)) if j != i])
        
        # 5. compute the distribution of probabilities of profile p on all k-mers of string i
        #    by calling score_profile() on all positions j in 0...n-k
        d = []
        for z in range(len(S[i])-k+1):                                    
            d.append(score_profile(S[i][z:z+k], p))   

        # 6. generate a random position according to the distribution d
        sum_of_distr = sum(d)
        if sum_of_distr == 0: # if the probabilities are all zero, choose uniformily at random
            randpos = random.randrange(n-k+1)
        else: # scale the distribution so that it is sums up to 1.0
            d = [x/sum_of_distr for x in d]
            r = random.random()
            f = 0
            for x in range(len(d)):
                f += d[x]
                if f >= r:
                    randpos = x
                    break        
        # 7. update the k-mer for the i-th string
        m[i] = S[i][randpos:randpos+k]
    return best

## MAIN
f = open("test.txt", "r")
dataset = ''
for x in f:
    dataset += x
# print(dataset)

# parse the input
dataset = dataset.strip().split('\n')
k, t, N = list(map(int, (dataset[0].split(' '))))
S = dataset[1].split(' ')
assert(len(S)==t)

# we remember the optimal motif in best
best = (0, [])

# run Gibbs sampler with 100 random re-starts
for _ in range(100):
    r = GibbsSampler(S, k, t, N)
    if r[0] > best[0]:
        best = r
print(best[0],' '.join(best[1]))