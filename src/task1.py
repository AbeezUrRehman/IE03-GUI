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

# The main function reads the input, calculates the similarity scores, and prints the user ID and similarity score.
def main():
    import sys
    file_path = sys.argv[1]
    N, M, ratings = read_input(file_path)
    similarity_scores = calculate_similarity(ratings, N, M)
    for user_id, score in similarity_scores:
        print(f"{user_id} {score:.16f}")

if __name__ == "__main__":
    main()
