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

def prefix_matching(trie, word):
    """ Return a pair (boolean, string) where <boolean> is True if-and-only-if a prefix of <word> appears in the <trie>
    and <string> is the pattern that matched the prefix  """
    temp = trie.copy()
    for i, letter in enumerate(word):
        if letter in temp.keys():
            temp = temp[letter]
            if "/" in temp.keys(): # check if match
                return True, word[:i+1]
        # if condition fail, no match found
        else:
            return False, word
    return False, word  # when word ends early traversing trie
            
     
file = open("dataset_675839_4.txt", "r")         # open a space-separated collection of strings 
text = file.readline().strip()   # text is on the first line
words = file.readline().strip().split(' ')      # create the list of words by splitting over spaces but first remove the newline if any

# print(words)

hits = {}                        # save the hits for each pattern in a dictionary, where the key is the word
for word in words:                   # for the example in Stepik we expect that hits = {'ATCG': [1, 11], 'GGGT': [4, 15]}
    hits[word] = []              # initially each pattern has an empty list of occurrences, we will append to these
    
trie = make_trie(words)              # create the trie using the code in the previous problem

# call prefix_matching(trie, ?) iteratively on each suffix of <text> 
# save the occurrences of each pattern in the dictionary <hits>
for i in range(len(text)):
    is_match,pattern = prefix_matching(trie, text[i:])
    if is_match:
       hits[pattern].append(i)

for word in hits:
    print(word + ': '+' '.join(map(str,hits[word]))) # print the list of hits according to the required format
    #print(word + ': '+' '.join(map(str,hits[word])), file = outFile) # print the list of hits according to the required format


# outFile.close()