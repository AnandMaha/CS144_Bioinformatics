# no ML libraries allowed, numpy OK
import math

def viterbi(s, states, start_p, trans_p, emit_p):
    """ computes the most probable path for string s """
    V = [{} for i in range(len(s))]   # dynamic programming table in log form to minimize the chances of underflow
    path = [] # list for printing out max weight path/states
    
    # Initialize base cases 
    max_p = -1
    for y in states:
        V[0][y] = math.log(start_p[y] * emit_p[y][s[0]]+1) # always store positive values in table
        max_p = V[0][y] if max_p < V[0][y] else max_p

    # Run Viterbi for the rest of the columns of the dynamic programming matrix
    for i in range(1, len(s)):
        for x in states: # curr state
            max_p = -1
            for y in states: # prev state
                temp_prob = math.log(V[i-1][y] * trans_p[y][x] * emit_p[x][s[i]]+1) 
                max_p = temp_prob if max_p < temp_prob else max_p
            V[i][x] = max_p # most weight from all possible prev states
        
    # start from the bottom tracing up
    max_state = ""
    max_p = -1
    for x in states:
        (max_state,max_p) = (x,V[len(s)-1][x]) if max_p < V[len(s)-1][x] else (max_state,max_p)
    path.append(max_state)
    for i in range(len(s)-2,-1,-1): # check if curr row calc == correct prob in next row
        for x in states:
            temp = math.log(V[i][x] * trans_p[x][max_state] * emit_p[max_state][s[i+1]]+1)
            if temp == max_p:
                max_p = V[i][x]
                max_state = x
                break
        path.append(max_state)
               
    path_str = ''.join(map(str,path))
    path_str = path_str[::-1] # states were appended in reverse
    return path_str

def readinput2(file):
    """ process the file describing the HMM as produced by stepik;
        returns observations, alphabet, states, initial probabilities, transition probabilities
        and emission probabilities """
    f = open(file, "r")
    dataset = ''
    for x in f:
        dataset += x
    dataset = dataset.replace("\t"," ")
    observations, alphabet, states, trans, emi = dataset.split('--------')
    observations = list(observations.strip())
    states = states.strip().split(' ')
    translist = trans.strip().split("\n")[1:]
    trans_dict = {}
    alphabet = alphabet.strip().split(" ")
    for i in range(len(translist)):
        trans_dict[states[i]] = {}
        temp = list(map(float,translist[i].strip().split(' ')[1:]))
        for s in range(len(states)):
            trans_dict[states[i]][states[s]]=temp[s]
    emilist = emi.strip().split('\n')[1:]
    emi_dict = {}
    num_emistates = len(emilist[0].strip().split(' ')[1:])
    for i in range(len(emilist)):
        emi_dict[states[i]] = {}
        temp = list(map(float,emilist[i].strip().split(' ')[1:]))
        for s in range(num_emistates):
            emi_dict[states[i]][alphabet[s]]=temp[s]
    # initial probabilities are all equal
    initial_probs = {}
    for i in trans_dict:
        initial_probs[i] = 1.0/len(trans_dict)
    f.close()
    return (observations, alphabet, states, initial_probs, trans_dict, emi_dict)

# ---- MAIN
string, alphabet, states, initial_probs, trans_dict, emi_dict = readinput2("test.txt")
print('string =',string)
print('alphabet =',alphabet)
print('states =',states)
print('initial probabilities =',initial_probs)
print('transition probabilities =',trans_dict)
print('emission probabilities =',emi_dict)
print('the most probable path is',viterbi(string, states, initial_probs, trans_dict, emi_dict))