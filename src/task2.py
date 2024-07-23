# numpy library is used for numerical operations
import numpy as np

# The read_input function reads the input from stdin and returns the number of users, the number of books, and the ratings matrix.
def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        N, M = map(int, lines[0].split())
        ratings = [list(map(float, line.split())) for line in lines[1:N+1]]
    return N, M, ratings

# The calculate_similarity function calculates the similarity scores between User 1 and other users. The similarity score is calculated using the Euclidean distance.
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

# The recommend_books function recommends books to User 1 based on the similarity scores. The function calculates the scores for each book and sorts them in descending order.
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

# The main function reads the input, calculates the similarity scores, and recommends books to User 1.
def main():
    import sys
    file_path = sys.argv[1]
    N, M, ratings = read_input(file_path)
    similarity_scores = calculate_similarity(ratings, N, M)
    recommendations = recommend_books(similarity_scores, ratings, M)
    for book_id, score in recommendations:
        print(f"{book_id} {score:.16f}")

if __name__ == "__main__":
    main()
