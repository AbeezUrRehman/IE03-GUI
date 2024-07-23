import numpy as np


def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        N, M, num_ratings = map(int, lines[0].split())  # Number of users and books
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

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python task4.py <input_file>")
        return

    file_path = sys.argv[1]
    N, M, ratings = read_input(file_path)
    
    while True:
        command = input("Enter command: ")
        if command == "exit":
            break
        parts = command.split()
        cmd = parts[0]
        if cmd == "rec":
            user_id = int(parts[1]) - 1
            if user_id >= N or user_id < 0:
                print("user not found.")
                continue
            if len(parts) == 2:
                similarity_scores = calculate_similarity(ratings, user_id, N, M)
                recommendations = recommend_books(similarity_scores, ratings, user_id, M)
                if recommendations:
                    for book_id, score in recommendations:
                        print(f"{book_id} {score:.16f}")
                else:
                    print("no appropriate item")
            elif len(parts) == 3:
                j = int(parts[2]) - 1
                similarity_scores = calculate_similarity(ratings, user_id, N, M)
                recommendations = recommend_books(similarity_scores, ratings, user_id, M)
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
            ratings[user_id, book_id] = rating
        else:
            print("invalid command")

if __name__ == "__main__":
    main()
