class UnionFind:
    def __init__(self, size):
        self.root = [i for i in range(size)]
        self.rank = [1] * size

    def find(self, x):
        if self.root[x] != x:
            self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.root[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.root[rootX] = rootY
            else:
                self.root[rootY] = rootX
                self.rank[rootX] += 1

    def connected(self, x, y):
        return self.find(x) == self.find(y)

def process_task5(input_data):
    lines = input_data.strip().split('\n')

    # First line contains N and R
    first_line = lines[0].strip().split()
    N = int(first_line[0])  # Number of users
    R = int(first_line[1])  # Number of friendship relations
    if not (2 <= N <= 100000):
        raise ValueError(f"N must be between 2 and 100000, got {N}")
    if not (1 <= R <= 100000):
        raise ValueError(f"R must be between 1 and 100000, got {R}")

    # Create an instance of UnionFind
    uf = UnionFind(N + 1)  # +1 because user index starts from 1

    # Process each friendship relation
    index = 1
    for _ in range(R):
        u, v = map(int, lines[index].strip().split())
        uf.union(u, v)
        index += 1

    # Next line contains Q, the number of queries
    Q = int(lines[index].strip())
    if not (1 <= Q <= 100000):
        raise ValueError(f"R must be between 1 and 100000, got {Q}")
    index += 1

    # Process each query
    results = []
    for _ in range(Q):
        u, v = map(int, lines[index].strip().split())
        if uf.connected(u, v):
            results.append('yes')
        else:
            results.append('no')
        index += 1

    return results
