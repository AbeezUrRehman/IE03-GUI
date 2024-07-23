import numpy as np

def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        first_line = lines[0].split()
        N = int(first_line[0])  # Number of users
        M = int(first_line[1])  # Number of books
        num_entries = int(first_line[2])  # Number of ratings provided
        ratings = np.full((N, M), -1.0)  # Initialize the ratings matrix with -1

        for line in lines[1:num_entries+1]:
            user, book, rating = line.split()
            user = int(user) - 1  # Convert 1-based index to 0-based
            book = int(book) - 1  # Convert 1-based index to 0-based
            ratings[user, book] = float(rating)

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

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python task3.py <input_file>")
        return

    file_path = sys.argv[1]
    N, M, ratings = read_input(file_path)
    similarity_scores = calculate_similarity(ratings, N, M)
    recommendations = recommend_books(similarity_scores, ratings, M)
    for book_id, score in recommendations:
        print(f"{book_id} {score:.16f}")

if __name__ == "__main__":
    main()
