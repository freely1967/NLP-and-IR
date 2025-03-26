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
            documents[file_name] = f.read()

# Function to show file content in a new window
def open_file_content(filename):
    if filename not in documents:
        messagebox.showerror("Error", f"File '{filename}' not found.")
        return

    # Create new window
    file_window = tk.Toplevel(root)
    file_window.title(filename)
    file_window.geometry("600x400")

   
    text_area = tk.Text(file_window, wrap="word", height=20, width=70)
    text_area.insert("1.0", documents[filename])
    text_area.config(state="disabled") 
    text_area.pack(padx=10, pady=10, fill="both", expand=True)


def perform_search():
    query = query_entry.get().strip()
    search_type = search_type_var.get()

    if not query:
        messagebox.showwarning("Input Error", "Please enter a search query.")
        return

    results_listbox.delete(0, tk.END)

  
    matches = boolean_search(query, documents)

    if not matches:
        results_listbox.insert(tk.END, "No match found.")
        return

    if search_type == "Boolean Search":
        results_listbox.insert(tk.END, f"Matches ({len(matches)}):")
        for match in matches:
            results_listbox.insert(tk.END, match)

    elif search_type == "Boolean + Ranked Search":
        filtered_docs = {doc: documents[doc] for doc in matches}
        ranked_results = ranked_search(query, filtered_docs)

        if not ranked_results:
            results_listbox.insert(tk.END, "No ranking results found.")
            return

        results_listbox.insert(tk.END, "Ranked Results:")
        for rank, (doc, score) in enumerate(ranked_results, 1):
            results_listbox.insert(tk.END, f"{rank}. {doc} (Score: {score:.4f})")

# selecting an item in the listbox
def on_result_select(event):
    try:
        selected_item = results_listbox.get(results_listbox.curselection())

        # Remove ranking number if present (e.g., "1. song.txt (Score: 0.4567)") so the date is "clickable"
        if ". " in selected_item:  
            selected_item = selected_item.split(". ", 1)[1]  

        # Remove score part if present -"-
        filename = selected_item.split(" (Score:")[0].strip()

        if filename and filename in documents:
            open_file_content(filename)
    except IndexError:
        pass 


root = tk.Tk()
root.title("Search UI")
root.geometry("500x400")

search_type_var = tk.StringVar(value="Boolean Search")
ttk.Label(root, text="Search Type:").pack(pady=5)
search_type_menu = ttk.Combobox(root, textvariable=search_type_var, values=["Boolean Search", "Boolean + Ranked Search"], state="readonly")
search_type_menu.pack()

ttk.Label(root, text="Enter Query:").pack(pady=5)
query_entry = ttk.Entry(root, width=50)
query_entry.pack(pady=5)

search_button = ttk.Button(root, text="Search", command=perform_search)
search_button.pack(pady=10)

ttk.Label(root, text="Results:").pack()
results_listbox = tk.Listbox(root, width=60, height=15)
results_listbox.pack(pady=5)
results_listbox.bind("<<ListboxSelect>>", on_result_select)  # Bind click event

root.mainloop()
