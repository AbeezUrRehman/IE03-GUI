import os
import argparse

def read_files(directory):
    pages = {}
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                content = file.read().split()
                keywords = [word for word in content if not word.endswith(".html")]
                links = [word for word in content if word.endswith(".html")]
                pages[filename] = {"keywords": keywords, "links": links}
    return pages

def initialize_scores(pages):
    num_pages = len(pages)
    scores = {page: 1.0 / num_pages for page in pages}
    return scores

def update_scores(pages, scores, iterations=20, damping_factor=0.85):
    num_pages = len(pages)
    for _ in range(iterations):
        new_scores = {}
        for page in pages:
            new_score = (1 - damping_factor) / num_pages
            link_contributions = sum(scores[link] / len(pages[link]["links"]) for link in pages if page in pages[link]["links"])
            new_score += damping_factor * link_contributions
            new_scores[page] = new_score
        scores = new_scores
    return scores

def normalize_scores(scores):
    max_score = max(scores.values())
    normalized_scores = {page: score / max_score for page, score in scores.items()}
    return normalized_scores

def calculate_relevance_scores(pages, query):
    query_words = set(query.split())
    relevance_scores = {page: 0 for page in pages}
    for word in query_words:
        for page, data in pages.items():
            if word in data["keywords"]:
                relevance_scores[page] += 1
    return normalize_scores(relevance_scores)

def combine_scores(importance_scores, relevance_scores):
    combined_scores = {page: importance_scores.get(page, 0) + relevance_scores.get(page, 0) for page in importance_scores}
    return combined_scores

def print_scores(importance_scores, relevance_scores, combined_scores):
    sorted_scores = sorted(combined_scores.items(), key=lambda item: item[1], reverse=True)
    print("word : page : score")
    for page, score in sorted_scores:
        print(f"{relevance_scores.get(page, 0):.2f} : {importance_scores.get(page, 0):.2f} : {score:.2f} : {page}")

def main():
    parser = argparse.ArgumentParser(description='Search engine for HTML documents.')
    parser.add_argument('directory', type=str, help='Directory containing HTML documents')
    args = parser.parse_args()

    pages = read_files(args.directory)

    importance_scores = initialize_scores(pages)
    importance_scores = update_scores(pages, importance_scores)
    importance_scores = normalize_scores(importance_scores)

    while True:
        query = input("Enter query: ").strip()
        if not query:
            break
        relevance_scores = calculate_relevance_scores(pages, query)
        combined_scores = combine_scores(importance_scores, relevance_scores)
        print_scores(importance_scores, relevance_scores, combined_scores)

if __name__ == "__main__":
    main()