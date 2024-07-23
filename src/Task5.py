import argparse

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

def main():
    parser = argparse.ArgumentParser(description='Union-Find for friendship detection.')
    parser.add_argument('input_file', type=str, help='Input file containing friendship relations and queries')
    args = parser.parse_args()

    try:
        # Open and read the file
        with open(args.input_file, 'r') as file:
            lines = file.readlines()

        # First line contains N and R
        first_line = lines[0].strip().split()
        N = int(first_line[0])  # Number of users
        R = int(first_line[1])  # Number of friendship relations

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

        # Output results
        for result in results:
            print(result)

    except FileNotFoundError:
        print(f"Error: The file '{args.input_file}' does not exist.")
    except IndexError:
        print("Error: The file is not formatted correctly.")
    except ValueError:
        print("Error: Invalid data format in the file.")

if __name__ == '__main__':
    main()