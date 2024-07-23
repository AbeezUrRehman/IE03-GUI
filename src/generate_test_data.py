import argparse
import random
import numpy as np
import os

def generate_task1_input(N, M):
    ratings = np.random.randint(1, 6, size=(N, M)).astype(float)
    for i in range(N):
        for j in range(M):
            if random.random() < 0.1:
                ratings[i, j] = -1
    input_data = f"{N} {M}\n" + "\n".join(" ".join(map(str, row)) for row in ratings)
    return input_data

def generate_task2_input(N, M):
    return generate_task1_input(N, M)

def generate_task3_input(N, M, E):
    ratings = []
    for _ in range(E):
        u = random.randint(1, N)
        b = random.randint(1, M)
        p = round(random.uniform(1, 5), 1)
        ratings.append(f"{u} {b} {p}")
    input_data = f"{N} {M} {E}\n" + "\n".join(ratings)
    return input_data

def generate_task4_input(N, M, E):
    base_input = generate_task3_input(N, M, E)
    commands = [
        f"rec {random.randint(1, N)}",
        f"eval {random.randint(1, N)} {random.randint(1, M)} {round(random.uniform(1, 5), 1)}"
    ]
    input_data = base_input + "\n".join(commands)
    return input_data

def generate_task5_input(N, R, Q):
    friendships = []
    for _ in range(R):
        si = random.randint(1, N)
        ti = random.randint(1, N)
        friendships.append(f"{si} {ti}")
    queries = []
    for _ in range(Q):
        pi = random.randint(1, N)
        qi = random.randint(1, N)
        queries.append(f"{pi} {qi}")
    input_data = f"{N} {R}\n" + "\n".join(friendships) + f"\n{Q}\n" + "\n".join(queries)
    return input_data

def generate_task6_input(N, M, E, R):
    ratings = []
    for _ in range(E):
        u = random.randint(1, N)
        b = random.randint(1, M)
        p = round(random.uniform(0, 5), 1)
        ratings.append(f"{u} {b} {p}")
    friendships = []
    for _ in range(R):
        si = random.randint(1, N)
        ti = random.randint(1, N)
        friendships.append(f"{si} {ti}")
    input_data = f"{N} {M} {E}\n" + "\n".join(ratings) + f"\n{R}\n" + "\n".join(friendships)
    return input_data

def random_word():
    with open("/usr/share/dict/words") as f:
        words = f.read().splitlines()
    return random.choice(words)

def generate_task7_input(doc_count):
    os.makedirs('source', exist_ok=True)

    # Read the English word list
    with open("/usr/share/dict/words") as f:
        words = f.read().splitlines()

    filenames = [f"document_{i}.html" for i in range(doc_count)]

    for filename in filenames:
        num_keywords = random.randint(5, 10)
        num_links = random.randint(1, min(10, len(filenames) - 1))

        keywords = random.sample(words, num_keywords)
        overlapping_keywords = random.sample(words, random.randint(1, 10))  # Add 1 to 10 overlapping words
        keywords += overlapping_keywords
        random.shuffle(keywords)
        links = random.sample([f for f in filenames if f != filename], num_links)

        with open(os.path.join('source', filename), 'w') as file:
            file.write(" ".join(keywords) + "\n")
            file.write("\n".join(links) + "\n")

    return f"Generated {doc_count} documents in 'source' directory"

def generate_task8_input(doc_count):
    response = generate_task7_input(doc_count)
    return response

def main():
    parser = argparse.ArgumentParser(description='Generate task inputs.')
    parser.add_argument('task', choices=['task1', 'task2', 'task3', 'task4', 'task5', 'task6', 'task7', 'task8'], help='Task to generate input for')
    parser.add_argument('--N', type=int, default=5, help='Number of rows or users')
    parser.add_argument('--M', type=int, default=5, help='Number of columns or items')
    parser.add_argument('--E', type=int, default=10, help='Number of ratings (only for task3, task4, and task6)')
    parser.add_argument('--R', type=int, default=10, help='Number of friendships (only for task5 and task6)')
    parser.add_argument('--Q', type=int, default=5, help='Number of queries (only for task5)')
    parser.add_argument('--doc_count', type=int, default=10, help='Number of documents (only for task7 and task8)')

    args = parser.parse_args()

    if args.task == 'task1' or args.task == 'task2':
        response = generate_task1_input(args.N, args.M)
        filename = f'{args.task}_input.txt'
    elif args.task == 'task3' or args.task == 'task4':
        response = generate_task3_input(args.N, args.M, args.E)
        filename = f'{args.task}_input.txt'
    elif args.task == 'task5':
        response = generate_task5_input(args.N, args.R, args.Q)
        filename = 'task5_input.txt'
    elif args.task == 'task6':
        response = generate_task6_input(args.N, args.M, args.E, args.R)
        filename = 'task6_input.txt'
    elif args.task == 'task7':
        response = generate_task7_input(args.doc_count)
        filename = None
    elif args.task == 'task8':
        response = generate_task8_input(args.doc_count)
        filename = None
    else:
        response = "Invalid task"
        filename = None

    if filename:
        with open(filename, 'w') as file:
            file.write(response)
        print(f'Generated input for {args.task} and saved to {filename}')
    else:
        print(response)

if __name__ == "__main__":
    main()