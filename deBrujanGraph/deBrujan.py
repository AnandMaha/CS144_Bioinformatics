# networkx only
import networkx as nx

def deBruijn(l):
    """ Takes in input a list of strings l of length k and
        it returns a deBruijn multi-edge directed graph """
    g = nx.MultiDiGraph()      # we need directed multigraph because we can have multiple edges between two nodes
    
    # add edge for each k-mer prefix->suffix
    for a in l:
        a_pre = a[:-1]
        a_suf = a[1:]
        g.add_edge(a_pre, a_suf)
    return g
        
f = open("test.txt", "r")      # open the file
w = f.readline().strip().split(' ') # get the reads/words
g = deBruijn(w)                     # build the graph

outFile = open("test1.txt", "w") 
for node in g.nodes:
    temp = ""
    if len(g.edges(node)) > 0:
        temp += node + ":"
        for edge in g.edges(node):
            temp += " " + edge[1] 
        # print(temp)
        print(temp, file = outFile)

# sort file
f = open("test1.txt", "r")
outFile = open("test2.txt", "w") 
w = f.readlines()
w = [x.strip() for x in w]
w.sort()
for str in w:
    print(str , file = outFile)