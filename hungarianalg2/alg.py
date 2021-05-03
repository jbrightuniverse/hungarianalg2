"""
Hungarian Algorithm No. 6 by James Yuming Yu
Vancouver School of Economics, UBC
1 May 2021
Based on http://www.cse.ust.hk/~golin/COMP572/Notes/Matching.pdf, 
         https://montoya.econ.ubc.ca/Econ514/hungarian.pdf, 
         https://github.com/jbrightuniverse/hungarianalg, and 
         https://github.com/jbrightuniverse/FastHungarianAlgorithm
"""

import numpy as np

class Node:
    """A simple node for an alternating tree."""
    
    def __init__(self):
        self.in_tree = False
        self.parent = None

def hungarian(matrx):
    """Runs the Hungarian Algorithm on a given matrix and returns the optimal matching with potentials."""
    
    # Step 1: Prep matrix, get size
    matrx = np.array(matrx)
    size = matrx.shape[0]
    
    # Step 2: Generate trivial potentials
    rpotentials = []
    cpotentials = [0] * size
    for i in range(len(matrx)):
        # the row weight is the maximum revenue in a row
        rpotentials.append(max(matrx[i]))

    # Step 3: Initialize alternating tree
    matching = [-1] * size
    x_nodes = [Node() for i in range(size)]
    y_nodes = [Node() for i in range(size)]
    x_nodes[0].in_tree = True

    # helper sets for higher performance
    treed_x = {0}
    untreed_y = set(range(size))
    treed_y = set()

    # Step 4: Loop while our matching is too small
    while -1 in matching:
        # Step A: Find any neighbour in equality graph
        # where a row is in the tree and a col is not in the tree
        pair = None
        flag = False
        for x in treed_x:
            for y in untreed_y:
                if matrx[x, y] == rpotentials[x] + cpotentials[y]:
                    pair = [x, y]
                    flag = True
                    break
            if flag: break

        if not pair:
            # Step B: If all firms are in the tree, update potentials to get a new one
            big = np.inf
            # iterate over relevant pairs
            for dx in treed_x:
                for dy in untreed_y:
                    # find the difference and check if its smaller than any we found before
                    weight = matrx[dx, dy]
                    alpha = rpotentials[dx] + cpotentials[dy] - weight
                    if alpha < big:
                        big = alpha
                        pair = [dx, dy]

            # apply difference to potentials as needed
            for dx in treed_x:
                rpotentials[dx] -= big

            for dy in treed_y:
                cpotentials[dy] += big

        # by this point we either got a pair from the equality graph or expanded the equality graph to have a new pair
        if pair[1] not in matching:
            # Step D: Firm is not matched so add it to matching 
            matching[pair[0]] = pair[1]
            # Step E: Swap the alternating path in our alternating tree attached to the worker we matched
            source = pair[0]
            matched = 1
            while True:
                if matched:
                    if x_nodes[source].parent == None: break
                    above = x_nodes[source].parent
                else:
                    above = y_nodes[source].parent
                    matching[above] = source

                matched = 1 - matched
                source = above

            # Step F: Destroy the tree, go to Step 4 to check completion, and possibly go to Step A
            if -1 in matching:
                for i in range(size):
                  x_nodes[i].in_tree = False
                  x_nodes[i].parent = None
                  y_nodes[i].in_tree = False
                  y_nodes[i].parent = None
              
                free = matching.index(-1)
                x_nodes[free].in_tree = True
                treed_x = {free}
                untreed_y = set(range(size))
                treed_y = set()

        else:
            # Step C: Firm is matched so add it to the tree and go back to Step A
            wasMatchedTo = matching.index(pair[1])
            treed_x.add(wasMatchedTo)
            treed_y.add(pair[1])
            untreed_y.remove(pair[1])
            y_nodes[pair[1]].in_tree = True
            y_nodes[pair[1]].parent = pair[0]
            x_nodes[wasMatchedTo].in_tree = True
            x_nodes[wasMatchedTo].parent = pair[1]
    
    revenues = [matrx[i, matching[i]] for i in range(size)]
    class Result:
        """A simple response object."""

        def __init__(self, match, revenues, row_weights, col_weights, revenue_sum):
            self.match = match
            self.revenues = revenues
            self.row_weights = row_weights
            self.col_weights = col_weights
            self.revenue_sum = revenue_sum

        def __str__(self):
            size = len(self.match)
            maxlen = max(len(str(max(self.revenues))), len(str(min(self.revenues))))
            baselist = [[" "*maxlen for i in range(size)] for j in range(size)]
            for i in range(size):
                entry = self.match[i]
                baselist[entry[0]][entry[1]] = str(self.revenues[i]).rjust(maxlen)

            formatted_list = '\n'.join([str(row) for row in baselist])
            return f"Matching:\n{formatted_list}\n\nRow Potentials: {self.row_weights}\nColumn Potentials: {self.col_weights}"

    return Result([[i, matching[i]] for i in range(size)], revenues, rpotentials, cpotentials, sum(revenues))
