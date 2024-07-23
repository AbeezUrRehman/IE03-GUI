import numpy as np

def read_input(input_data):
    lines = input_data.split('\n')
    N, M = map(int, lines[0].split())
    if not (2 <= N <= 100):
        raise ValueError(f"N must be between 2 and 100, got {N}")
    if not (1 <= M <= 100):
        raise ValueError(f"M must be between 1 and 100, got {M}")
    ratings = [list(map(float, line.split())) for line in lines[1:N+1]]
    return N, M, ratings

def calculate_similarity(ratings, N, M):
    similarity_scores = []
    for i in range(1, N):  # Start from 1 to compare with User 1
        dist = 0
        common = False
        for j in range(M):
            if ratings[0][j] != -1 and ratings[i][j] != -1:
                dist += (ratings[0][j] - ratings[i][j]) ** 2
                common = True
        if common:
            dist = np.sqrt(dist)
            score = 1 / (1 + dist)
        else:
            score = 0
        similarity_scores.append((i + 1, score))
    return sorted(similarity_scores, key=lambda x: -x[1])

def process_task1(input_data):
    N, M, ratings = read_input(input_data)
    similarity_scores = calculate_similarity(ratings, N, M)
    return similarity_scores
