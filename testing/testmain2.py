import os
import tkinter as tk
from tkinter import ttk, messagebox
from boolean_search import boolean_search
from ranked_search import ranked_search

# Load documents
folder_path = os.path.join(os.getcwd(), "songs")

if not os.path.exists(folder_path):
    messagebox.showerror("Error", f"Folder '{folder_path}' not found.")
    exit()

documents = {}
for file_name in os.listdir(folder_path):
    if file_name.endswith(".txt"):
        with open(os.path.join(folder_path, file_name), "r", encoding="utf-8") as f:
            documents[file_name] = f.read().lower()

# Search function
def perform_search():
    query = query_entry.get().strip()
    search_type = search_type_var.get()

    if not query:
        messagebox.showwarning("Input Error", "Please enter a search query.")
        return

    results_listbox.delete(0, tk.END)

    # Boolean Search
    matches = boolean_search(query, documents)

    if not matches:
        results_listbox.insert(tk.END, "No match found.")
        return

    if search_type == "Boolean Search":
        results_listbox.insert(tk.END, f"Matches ({len(matches)}):")
        for match in matches:
            results_listbox.insert(tk.END, f"- {match}")

    elif search_type == "Boolean + Ranked Search":
        filtered_docs = {doc: documents[doc] for doc in matches}
        ranked_results = ranked_search(query, filtered_docs)

        if not ranked_results:
            results_listbox.insert(tk.END, "No ranking results found.")
            return

        results_listbox.insert(tk.END, "Ranked Results:")
        for rank, (doc, score) in enumerate(ranked_results, 1):
            results_listbox.insert(tk.END, f"{rank}. {doc} (Score: {score:.4f})")

# GUI Setup
root = tk.Tk()
root.title("Search UI")
root.geometry("500x400")

# Search Type Dropdown
search_type_var = tk.StringVar(value="Boolean Search")
ttk.Label(root, text="Search Type:").pack(pady=5)
search_type_menu = ttk.Combobox(root, textvariable=search_type_var, values=["Boolean Search", "Boolean + Ranked Search"], state="readonly")
search_type_menu.pack()

# Query Input
ttk.Label(root, text="Enter Query:").pack(pady=5)
query_entry = ttk.Entry(root, width=50)
query_entry.pack(pady=5)

# Search Button
search_button = ttk.Button(root, text="Search", command=perform_search)
search_button.pack(pady=10)

# Results Listbox
ttk.Label(root, text="Results:").pack()
results_listbox = tk.Listbox(root, width=60, height=15)
results_listbox.pack(pady=5)

# Run the GUI
root.mainloop()
