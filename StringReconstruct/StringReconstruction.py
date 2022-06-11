## networkx only
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

f = open("test.txt", "r")  # open the file
## YOUR CODE HERE
## Read the k-mer and the strings from the file
f.readline() # length of k-mer
w = f.readline().strip().split(' ') # list of k-mers
## Build the deBrujin graph on the strings
g = deBruijn(w)

## Find the Eulerian path and reconstruct/print the string
edges = []
for e in nx.eulerian_path(g):
    edges.append(e)
euler_path = ""
for i in range(len(edges)):
    if i == len(edges)-1:
        euler_path += edges[i][0] + " " + edges[i][1]
    else:
        euler_path += edges[i][0] + " "

# to reconstruct the string print the first letter of each (k-1)-mer
# except for the last one which will be printed in its entirety
final_str = ""
k_mers = euler_path.split(" ")
for i in range(len(k_mers)):
    if i == len(k_mers)-1:
        final_str += k_mers[i]
    else:
        final_str += k_mers[i][0]
        
outFile = open("test1.txt", "w")
print(final_str,end="", file = outFile)
# print(final_str,end="")