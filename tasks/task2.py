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
    for i in range(1, N):  # Skip User 1 since we compare others to User 1
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
        similarity_scores.append((i, score))
    return similarity_scores

def recommend_books(similarity_scores, ratings, M):
    user_books = [j for j in range(M) if ratings[0][j] == -1]
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

def process_task2(input_data):
    N, M, ratings = read_input(input_data)
    similarity_scores = calculate_similarity(ratings, N, M)
    recommendations = recommend_books(similarity_scores, ratings, M)
    return recommendations
