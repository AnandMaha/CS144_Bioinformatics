# no libraries allowed except for numpy (if needed)

def PHP(path, trans, initial_prob):
    """ 
        path: list, t: dictionary, i float
    computes the probability of the path from
        transition matrix and the initial probability"""
    php = initial_prob
    for i in range(len(path)-1):
        php *= trans[path[i]][path[i+1]]
    
    return php

def readinput1(file):
    """ process the file describing the input to the problem as produced by stepik;
        returns path, transition probabilities, and the initial probability for each state """
    f = open(file, "r")
    input = ''
    for x in f:
        input += x
    input = input.replace("\t"," ")
    path, states, trans = input.split('--------')
    path = list(path.strip())
    states = states.strip().split(' ')
    translist = trans.strip().split("\n")
    translist = translist[1:]
    trans_dict = {}
    for i in range(len(translist)):
        trans_dict[states[i]] = {}
        temp = list(map(float,translist[i].strip().split(' ')[1:]))
        for s in range(len(states)):
            trans_dict[states[i]][states[s]]=temp[s]
    #we assume initial probability is the same for each state, that is 1.0/len(trans_dict)
    return path, trans_dict, 1.0/len(trans_dict)

# get the parameters of the problem
# p list, t dictionary, i float
p, t, i = readinput1("test.txt")
print('The path is',p)
print('Transition matrix is', t)
print('The initial probability for each state is',i)
# computes the probability of the path
print('The probability of',''.join(p),'is', PHP(p,t,i))