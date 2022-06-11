## no tree/graph/tries libraries allowed
## code adapted from https://nbviewer.jupyter.org/gist/BenLangmead/6665861

class SuffixTree(object):
    
    class Node(object):
        def __init__(self, lab):
            self.lab = lab # edge label
            self.out = {}  # outgoing edges; maps characters to nodes
        
        def traverse(self,level):
            """ Traverse the suffix tree in DFS order and prints the
                label on the edges with their level number """
            for x in self.out:          # x is the first letter of the outgoing edge, if self.out=={} we are in a leaf and the for loop is not executed
                child = self.out[x]     # out[x] gives the pointer to the children with an edge that starts with x
                print(level,child.lab)
                child.traverse(level+1) # visit recursively the child

        def longestRepeat(self,s):
            global longest
            """ Finds the longest repeated string by finding the internal node in the suffix
                tree that corresponds to the longest string from the root"""
            ## this function is almost identical to traverse()
            ## start with traverse() as a template, and save in the global variable <longest> the
            ## longest repeated string encountered so far during the traversal

            # STRATEGY: Get substring of deepest (num. characters) forking internal node
            
            for x in self.out:          # x is the first letter of the outgoing edge, if self.out=={} we are in a leaf and the for loop is not executed
                if len(self.out) > 1 and len(s) > len(longest):
                    longest = s
                child = self.out[x]     # out[x] gives the pointer to the children with an edge that starts with x
                child.longestRepeat(s+child.lab if "$" not in child.lab else s) # visit recursively the child

    def __init__(self, s):
        """ Make suffix tree, without suffix links, from s in quadratic time
            and linear space """
        s += '$'
        self.root = self.Node(None)
        self.root.out[s[0]] = self.Node(s) # trie for just longest suf
        # add the rest of the suffixes, from longest to shortest
        for i in range(1, len(s)):
            # start at root; we’ll walk down as far as we can go
            cur = self.root
            j = i
            while j < len(s):
                if s[j] in cur.out:
                    child = cur.out[s[j]]
                    lab = child.lab
                    # Walk along edge until we exhaust edge label or
                    # until we mismatch
                    k = j+1 
                    while k-j < len(lab) and s[k] == lab[k-j]:
                        k += 1
                    if k-j == len(lab):
                        cur = child # we exhausted the edge
                        j = k
                    else:
                        # we fell off in middle of edge
                        cExist, cNew = lab[k-j], s[k]
                        # create “mid”: new node bisecting edge
                        mid = self.Node(lab[:k-j])
                        mid.out[cNew] = self.Node(s[k:])
                        # original child becomes mid’s child
                        mid.out[cExist] = child
                        # original child’s label is curtailed
                        child.lab = lab[k-j:]
                        # mid becomes new child of original parent
                        cur.out[s[j]] = mid
                else:
                    # Fell off tree at a node: make new edge hanging off it
                    cur.out[s[j]] = self.Node(s[j:])
    
    def followPath(self, s):
        """ Follow path given by s.  If we fall off tree, return None.  If we
            finish mid-edge, return (node, offset) where 'node' is child and
            'offset' is label offset.  If we finish on a node, return (node,
            None). """
        cur = self.root
        i = 0
        while i < len(s):
            c = s[i]
            if c not in cur.out:
                return (None, None) # fell off at a node
            child = cur.out[s[i]]
            lab = child.lab
            j = i+1
            while j-i < len(lab) and j < len(s) and s[j] == lab[j-i]:
                j += 1
            if j-i == len(lab):
                cur = child # exhausted edge
                i = j
            elif j == len(s):
                return (child, j-i) # exhausted query string in middle of edge
            else:
                return (None, None) # fell off in the middle of the edge
        return (cur, None) # exhausted query string at internal node
    
    def hasSubstring(self, s):
        """ Return true iff s appears as a substring """
        node, off = self.followPath(s)
        return node is not None
    
    def hasSuffix(self, s):
        """ Return true iff s is a suffix """
        node, off = self.followPath(s)
        if node is None:
            return False # fell off the tree
        if off is None:
            # finished on top of a node
            return '$' in node.out
        else:
            # finished at offset 'off' within an edge leading to 'node'
            return node.lab[off] == '$'
           
    def traverse(self):
        return self.root.traverse(0)

    def longestRepeat(self):
        global longest
        longest = ''
        self.root.longestRepeat('')
        print(longest)

    

f = open("dataset_675839_4.txt", "r")         # open the file
text = f.readline().strip()            # text is on the first line

# MAKE THE SUFFIX TREE
stree = SuffixTree(text)
#stree.traverse()
stree.longestRepeat()