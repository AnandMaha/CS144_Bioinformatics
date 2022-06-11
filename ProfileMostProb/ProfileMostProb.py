# no libraries allowed, except for biopython and numpy, if wanted

def score_profile(s, p):
    """ computes the probability of string s using the profile p """
    prob = p[0][s[0]]
    for i in range(1, len(s)):
        prob *= p[i][s[i]]
    return prob

# read the file
f = open("test.txt", "r")
dataset = ''
for x in f:
    dataset += x
# parse the input
dataset = dataset.splitlines()                                          
text = dataset[0]                                                       
k = int(dataset[1])                                                     
As = list(map(float, dataset[2].split())) # probabilities for As
Cs = list(map(float, dataset[3].split())) # probabilities for Cs
Gs = list(map(float, dataset[4].split())) # probabilities for Gs
Ts = list(map(float, dataset[5].split())) # probabilities for Ts
# build the PWM p as an array of dictionaries
p = []                                                                  
for i in range(len(As)):                                               
    p.append({'A': As[i], 'C': Cs[i], 'G': Gs[i], 'T': Ts[i]})
# keep track of the best scoring position in the variable best
# best[0] contains the score, and best[1] the best k-mer
best = (-1, '')                                                         
for i in range(len(text)-k+1):                                        
    score = score_profile(text[i:i+k], p)                               
    if score > best[0]:                                                 
        best = (score, text[i:i+k])
print(best[1])