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

def read_input(file):
    N, M, num_ratings = map(int, file.readline().strip().split())  # Number of users and books
    ratings = [[-1.0 for _ in range(M)] for _ in range(N)]  # Initialize ratings matrix with -1
    for _ in range(num_ratings):
        user, book, rating = map(float, file.readline().strip().split())
        ratings[int(user) - 1][int(book) - 1] = rating
    return N, M, ratings

def read_friendships(file):
    R = int(file.readline().strip())  # Number of friendship relations
    friendships = []
    for _ in range(R):
        u, v = map(int, file.readline().strip().split())
        friendships.append((u - 1, v - 1))
    return friendships

def calculate_similarity(ratings, user_id, N, M, friends):
    similarity_scores = []
    for i in range(N):
        if i != user_id and friends[i]:
            dist = 0
            common = False
            for j in range(M):
                if ratings[user_id][j] != -1 and ratings[i][j] != -1:
                    dist += (ratings[user_id][j] - ratings[i][j]) ** 2
                    common = True
            if common:
                dist = dist ** 0.5
                score = 1 / (1 + dist)
            else:
                score = 0
            similarity_scores.append((i, score))
    return similarity_scores

def recommend_books(similarity_scores, ratings, user_id, M):
    user_books = [j for j in range(M) if ratings[user_id][j] == -1]
    book_scores = {book: 0 for book in user_books}
    total_similarity = {book: 0 for book in user_books}

    for user_index, sim_score in similarity_scores:
        for book in user_books:
            if ratings[user_index][book] != -1:
                book_scores[book] += ratings[user_index][book] * sim_score
                total_similarity[book] += sim_score

    final_scores = []
    for book in user_books:
        if total_similarity[book] > 0:
            final_score = book_scores[book] / total_similarity[book]
        else:
            final_score = 0
        final_scores.append((book + 1, final_score))

    final_scores.sort(key=lambda x: -x[1])
    return final_scores

def main():
    parser = argparse.ArgumentParser(description='Recommendation system with Union-Find.')
    parser.add_argument('input_file', type=str, help='Input file containing users, books, ratings, and friendships data')
    args = parser.parse_args()

    with open(args.input_file, 'r') as file:
        N, M, ratings = read_input(file)
        friendships = read_friendships(file)

    uf = UnionFind(N)
    for u, v in friendships:
        uf.union(u, v)

    while True:
        command = input().strip()
        if command == "exit":
            break
        parts = command.split()
        cmd = parts[0]
        if cmd == "rec":
            user_id = int(parts[1]) - 1
            if user_id >= N or user_id < 0:
                print("user not found.")
                continue

            friends = [uf.connected(user_id, i) for i in range(N)]
            similarity_scores = calculate_similarity(ratings, user_id, N, M, friends)
            recommendations = recommend_books(similarity_scores, ratings, user_id, M)
            if len(parts) == 2:
                if recommendations:
                    for book_id, score in recommendations:
                        print(f"{book_id} {score:.16f}")
                else:
                    print("no appropriate item")
            elif len(parts) == 3:
                j = int(parts[2]) - 1
                if j < len(recommendations):
                    book_id, score = recommendations[j]
                    print(f"{book_id} {score:.16f}")
                else:
                    print("no appropriate item")
        elif cmd == "eval":
            user_id = int(parts[1]) - 1
            book_id = int(parts[2]) - 1
            rating = float(parts[3])
            if user_id >= N or user_id < 0 or book_id >= M or book_id < 0:
                print("invalid input")
                continue
            ratings[user_id][book_id] = rating
        else:
            print("invalid command")

if __name__ == "__main__":
    main()