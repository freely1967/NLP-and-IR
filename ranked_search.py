import os
import math
import re
from collections import Counter

def preprocess(text):
    """Converts text to lowercase and removes special characters."""
    return re.sub(r'\W+', ' ', text.lower())

def compute_tf(doc):
    """Computes Term Frequency (TF) for a document."""
    words = doc.split()
    total_words = len(words)
    tf = Counter(words)
    return {word: count / total_words for word, count in tf.items()}

def compute_idf(docs):
    """Computes Inverse Document Frequency (IDF) for all terms in the corpus."""
    num_docs = len(docs)
    idf = {}
    all_terms = set(word for doc in docs.values() for word in doc.split())

    for term in all_terms:
        containing_docs = sum(1 for doc in docs.values() if term in doc.split())
        idf[term] = math.log(num_docs / (1 + containing_docs))  # Using log(N / (1 + df))

    return idf

def compute_tfidf(docs):
    """Computes TF-IDF scores for all documents."""
    tfidf_scores = {}
    idf = compute_idf(docs)

    for title, content in docs.items():
        tf = compute_tf(content)
        tfidf_scores[title] = {word: tf[word] * idf[word] for word in tf}

    return tfidf_scores

def ranked_search(query, docs):
    """Performs ranked search using TF-IDF scoring."""
    query_terms = preprocess(query).split()
    tfidf_scores = compute_tfidf(docs)
    
    doc_scores = {}

    for doc, tfidf in tfidf_scores.items():
        score = sum(tfidf.get(term, 0) for term in query_terms)
        if score > 0:
            doc_scores[doc] = score

    ranked_results = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

    return ranked_results

if __name__ == "__main__":
    folder_path = os.path.join(os.getcwd(), "songs")

    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        exit()

    documents = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            with open(os.path.join(folder_path, file_name), "r", encoding="utf-8") as f:
                documents[file_name] = preprocess(f.read())

    query = input("Search-Query: ")
    results = ranked_search(query, documents)

    if results:
        print("\nRanked Results:")
        for rank, (doc, score) in enumerate(results, 1):
            print(f"{rank}. {doc} (Score: {score:.4f})")
    else:
        print("No match found.")
