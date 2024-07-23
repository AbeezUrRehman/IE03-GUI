import numpy as np

def read_input(input_data):
    lines = input_data.split('\n')
    N, M, num_ratings = map(int, lines[0].split())  # Number of users, books, and ratings
    if not (2 <= N <= 100000):
        raise ValueError(f"N must be between 2 and 100000, got {N}")
    if not (1 <= M <= 100000):
        raise ValueError(f"M must be between 1 and 100000, got {M}")
    if not (0 <= num_ratings <= 100000):
        raise ValueError(f"E must be between 0 and 100000, got {num_ratings}")
    ratings = np.full((N, M), -1.0)  # Initialize ratings matrix with -1

    for line in lines[1:num_ratings+1]:
        user, book, rating = map(float, line.split())
        ratings[int(user)-1, int(book)-1] = rating

    return N, M, ratings

def calculate_similarity(ratings, user_id, N, M):
    similarity_scores = []
    for i in range(N):
        if i != user_id:
            dist = 0
            common = False
            for j in range(M):
                if ratings[user_id][j] != -1 and ratings[i][j] != -1:
                    dist += (ratings[user_id][j] - ratings[i][j]) ** 2
                    common = True
            if common:
                dist = np.sqrt(dist)
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

def process_task4(input_data):
    N, M, ratings = read_input(input_data)
    return N, M, ratings

def evaluate_command(command, ratings, N, M):
    parts = command.split()
    cmd = parts[0]
    if cmd == "rec":
        user_id = int(parts[1]) - 1
        if user_id >= N or user_id < 0:
            return ["user not found."]
        if len(parts) == 2:
            similarity_scores = calculate_similarity(ratings, user_id, N, M)
            recommendations = recommend_books(similarity_scores, ratings, user_id, M)
            if recommendations:
                return [f"{book_id} {score:.16f}" for book_id, score in recommendations]
            else:
                return ["no appropriate item"]
        elif len(parts) == 3:
            j = int(parts[2]) - 1
            similarity_scores = calculate_similarity(ratings, user_id, N, M)
            recommendations = recommend_books(similarity_scores, ratings, user_id, M)
            if j < len(recommendations):
                book_id, score = recommendations[j]
                return [f"{book_id} {score:.16f}"]
            else:
                return ["no appropriate item"]
    elif cmd == "eval":
        user_id = int(parts[1]) - 1
        book_id = int(parts[2]) - 1
        rating = float(parts[3])
        if user_id >= N or user_id < 0 or book_id >= M or book_id < 0:
            return ["invalid input"]
        ratings[user_id, book_id] = rating
        return ["Rating updated"]
    else:
        return ["invalid command"]
