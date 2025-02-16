import hashlib

class Merkle:
    def __init__(self, base=[], verbose=0):
        self.base = base
        self.verbose = verbose
        self.tree = []
        self.num_leaves = len(self.base)
        if not self.base:
            return
        else:
            self.create_tree()
            self.route_proof()

    def route_proof(self):
        start_time = time.time()
        self.auth_lists = []
        
        if self.verbose == 1:
            print('Calculating proofs: tree height ', str(self.height), ',', str(self.num_leaves), ' leaves')

        for y in range(self.num_leaves):
            auth_route = []
            leaf = self.tree[0][y]
            for x in range(self.height):      
                if len(self.tree[x]) == 1:    
                    if self.tree[x] == self.root:       
                        auth_route.append(self.root)    
                        self.auth_lists.append(auth_route)
                    else:
                        print('Merkle route calculation failed @ root')   
                else:
                    nodes = self.tree[x]
                    nodes_above = self.tree[x+1]      
                    for node in nodes:          
                        if leaf != node:
                            for nodehash in nodes_above:
                                if hashlib.sha256(leaf + node).hexdigest() == nodehash:
                                    auth_route.append((leaf, node))         #binary hash is ordered
                                    leaf = nodehash
                                elif hashlib.sha256(node + leaf).hexdigest() == nodehash:
                                    auth_route.append((node, leaf))
                                    leaf = nodehash
                                else:
                                    pass
        elapsed_time = time.time() - start_time
        if self.verbose == 1:
            print(elapsed_time)   
        
        return

    def create_tree(self):
        if self.num_leaves <= 2:
            num_branches = 1
        elif self.num_leaves > 2 and self.num_leaves <= 4:
            num_branches = 2
        elif self.num_leaves > 4 and self.num_leaves <= 8:
            num_branches = 3
        elif self.num_leaves > 8 and self.num_leaves <= 16:
            num_branches = 4
        elif self.num_leaves > 16 and self.num_leaves <= 32:
            num_branches = 5
        elif self.num_leaves > 32 and self.num_leaves <= 64:
            num_branches = 6
        elif self.num_leaves > 64 and self.num_leaves <= 128:
            num_branches = 7
        elif self.num_leaves > 128 and self.num_leaves <= 256:
            num_branches = 8
        elif self.num_leaves > 256 and self.num_leaves <= 512:
            num_branches = 9

        self.num_branches = num_branches
        self.tree.append(self.base)

        hashlayer = self.base

        for x in range(num_branches):       #iterate through each layer of the merkle tree starting with the base layer
            temp_array = []
            cycles = len(hashlayer) % 2 + len(hashlayer) // 2
            y = 0
            for x in range(cycles):
                if y + 1 == len(hashlayer):
                    temp_array.append(str(hashlayer[y]))
                else:
                    temp_array.append(hashlib.sha256(str(hashlayer[y]) + str(hashlayer[y + 1])).hexdigest())
                    y = y + 2

            self.tree.append(temp_array)
            hashlayer = temp_array
        self.root = temp_array
        self.height = len(self.tree)
        if self.verbose == 1:
            print('Merkle tree created with ' + str(self.num_leaves), ' leaves, and ' + str(self.num_branches) + ' to root.')
        return self.tree