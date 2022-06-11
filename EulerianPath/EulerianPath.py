## networkx only
import networkx as nx

f = open("test.txt", "r") # open the file
l = [x.strip() for x in f]     # read all lines, removing the newline at the end
g = nx.MultiDiGraph()

## YOUR CODE HERE
## First, parse the input file, and build the graph using nx
for line in l:
    # new list of line to add edges to graph
    edge_list = line.split(" ")
    edge_list[0] = edge_list[0].strip(":")
    for i in range(1, len(edge_list)):
        g.add_edge(edge_list[0], edge_list[i])

## Second, find an Eulerian path using nx, and print it
edges = []
for e in nx.eulerian_path(g):
    edges.append(e)
temp = ""
for i in range(len(edges)):
    if i == len(edges)-1:
        temp += edges[i][0] + " " + edges[i][1]
    else:
        temp += edges[i][0] + " "

outFile = open("test1.txt", "w")
print(temp, end="", file = outFile)
# print(temp, end="")