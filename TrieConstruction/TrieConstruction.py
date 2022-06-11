## no tree/graph/tries libraries allowed

# outFile = open('test.txt', "w")

def make_trie(words): 
    """ creates a trie (e.g., implemented as a nested dictionary) from a list of words """
    trie = {}

    for word in words:
        temp = trie
        for i, letter in enumerate(word): 
            if letter not in temp:
                temp[letter] = {}
            if i == len(word)-1:
                temp[letter]['/'] = {} # indicate end of word
            temp = temp[letter]
        
    # print(trie)
    return trie


def print_trie(trie): 
    """ prints the trie as an edge list according to the format required """
    print_trie_dfs(trie, 0, []) 
    

# par is parent node num, visited is list of nodes num visited
def print_trie_dfs(trie, par, visited): 
    for key in trie:
        if par not in visited:
            visited.append(par)
        if key != '/':
            chld = par+1
            while chld in visited: # choose node num diff from visited
                chld += 1
            
            print(str(par),str(chld),key)
            # print(str(par),str(chld),key, file = outFile)
            print_trie_dfs(trie[key], chld, visited)
    
            
file = open("dataset_675839_4.txt", "r")         # open a space-separated collection of strings 
words = file.readline().strip().split(' ')      # create the list of words by splitting over spaces but first remove the newline if any

# print(words)

print_trie(make_trie(words))
# outFile.close()