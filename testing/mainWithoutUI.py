"""Main script for the LR-Project"""
import os
from boolean_search import boolean_search  # Import Boolean Search
from ranked_search import ranked_search   # Import Ranked Search

# Relative path of all the songs
folder_path = os.path.join(os.getcwd(), "songs")

if not os.path.exists(folder_path):
    print(f"Error: Folder '{folder_path}' not found.")
    exit()

# Read and store documents
documents = {}
for file_name in os.listdir(folder_path):
    if file_name.endswith(".txt"):
        with open(os.path.join(folder_path, file_name), "r", encoding="utf-8") as f:
            documents[file_name] = f.read().lower() 

# Choose search type
print("Choose search type:")
print("1. Boolean Search")
print("2. Boolean + Ranked Search (Optimized)")
choice = input("Enter 1 or 2: ").strip()

if choice not in {"1", "2"}:
    print("Invalid choice. Please restart and enter 1 or 2.")
    exit()

# User enters search query
query = input("Enter your search query: ").strip()

# Perform Boolean Search
print("\nPerforming Boolean Search...\n")
matches = boolean_search(query, documents)

if not matches:
    print("No match found.")
    exit()

print(f"\nBoolean Search found {len(matches)} matching documents:")
for match in matches:
    print(f"- {match}")

# If user chose option 2, perform Ranked Search on matched documents
if choice == "2":
    print("\nPerforming Ranked Search on filtered results...\n")
    filtered_docs = {doc: documents[doc] for doc in matches}  # Use only matched documents
    results = ranked_search(query, filtered_docs)

    if results:
        print("\nRanked Results:")
        for rank, (doc, score) in enumerate(results, 1):
            print(f"{rank}. {doc} (Score: {score:.4f})")
    else:
        print("No ranking results found.")
