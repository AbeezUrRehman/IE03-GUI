import os

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

def get_scores(directory):
    pages = read_files(directory)
    scores = initialize_scores(pages)
    scores = update_scores(pages, scores)
    scores = normalize_scores(scores)
    return scores

def format_scores(scores):
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    formatted_scores = [f"{page}: {score:.2f}" for page, score in sorted_scores]
    return formatted_scores
