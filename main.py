import json
import tkinter as tk
from tkinter import ttk
import ssl
import nltk
import certifi

from graph import Graph
from review import Review
from select_asin import handle_asin_selection


def load_graph_from_json(file_path: str) -> tuple[Graph, set[str]]:
    """
    Loads json file data into graph object.

    Preconditions:
    - type(file_path) == str
    - len(file_path) > 0
    - file_path[-5:] == '.json'
    """
    g = Graph()

    asins = set()
    with open(file_path, 'r') as file:
        for line in file:
            all_data = json.loads(line)

            # add product
            asin = all_data['asin']
            if asin not in asins:
                asins.add(asin)
            if asin not in g.vertices:
                g.add_vertex(asin, 'product')

            # add review
            reviewer_id = all_data['reviewerID']
            if reviewer_id not in g.vertices:
                g.add_vertex(reviewer_id, 'reviewer')

            review = Review(
                all_data['overall'],
                all_data['reviewTime'],
                all_data['reviewText']
            )
            g.add_edge(asin, reviewer_id, review)

            assert g.adjacent(asin, reviewer_id)
    return g, asins

if __name__ == '__main__':
    # enables download of nltk corpuses on mac
    # source: https://medium.com/@ruheeh/installing-nltk-natural-language-toolkit-in-macos-catalina-10-15-aeb3bc6255a9
    ssl._create_default_https_context = ssl._create_unverified_context
    nltk.data.path.append(certifi.where())

    data_to_download = ['punkt', 'words', 'stopwords']
    for data in data_to_download:
        if not nltk.corpus.words.fileids():
            nltk.download(data)

    graph, all_asins = load_graph_from_json('appliances_data.json')

    # sets up tkinter window
    root = tk.Tk()
    root.title("Product Analysis Display")

    # CREATE DROP DOWN IN UPPER LEFT CORNER OF TKINTER WINDOW
    # 1) asin selection using combobox
    label = ttk.Label(root, text="Select the ASIN:", foreground="black", font=("Arial", 16))
    label.grid(row=0, column=1, padx=20, pady=20)

    asin_selected = tk.StringVar()
    asin_combobox = ttk.Combobox(root, width=27, textvariable=asin_selected, values=list(all_asins))
    asin_combobox.grid(column=1, row=1)
    asin_combobox.current(0)  # Set the current selection to the first item in the list if available

    # 2) button to get graphs
    update_button = ttk.Button(root, text="Select This Product",
                               command=lambda: handle_asin_selection(root, asin_combobox, graph))
    update_button.grid(row=2, column=1, pady=10)

    root.mainloop()
