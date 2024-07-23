import numpy as np

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

def read_input(input_data):
    lines = input_data.strip().split('\n')
    N, M, E = map(int, lines[0].strip().split())
    if not (2 <= N <= 100000):
        raise ValueError(f"N must be between 1 and 100000, got {N}")
    if not (1 <= M <= 100000):
        raise ValueError(f"M must be between 1 and 100000, got {M}")
    if not (0 <= E <= 100000):
        raise ValueError(f"E must be between 1 and 100000, got {E}")
    ratings = np.full((N, M), -1.0)
    index = 1
    for _ in range(E):
        u, b, p = map(float, lines[index].strip().split())
        ratings[int(u) - 1][int(b) - 1] = p
        index += 1
    R = int(lines[index].strip())
    index += 1
    friendships = []
    for _ in range(R):
        s, t = map(int, lines[index].strip().split())
        friendships.append((s - 1, t - 1))
        index += 1
    return N, M, ratings, friendships

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

def process_task6(input_data):
    user_id = 0  # Fixed to User 1 (0 in 0-based index)
    N, M, ratings, friendships = read_input(input_data)
    uf = UnionFind(N)
    for u, v in friendships:
        uf.union(u, v)

    friends = [uf.connected(user_id, i) for i in range(N)]
    similarity_scores = calculate_similarity(ratings, user_id, N, M, friends)
    recommendations = recommend_books(similarity_scores, ratings, user_id, M)
    return recommendations
