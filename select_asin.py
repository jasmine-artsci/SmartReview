import tkinter as tk

from typing import Any
from plotting import plot_sentiment_analysis_current_product, plot_average_sentiment_analysis_score
from plotting import plot_sentiment_distribution, generate_wordcloud_figure, generate_scatter_plot_figure
from plotting import display_figure

from graph import Graph
from text_analysis import clean_text, sentiment_analysis


def handle_asin_selection(root: tk.Tk, asin_combobox: Any, graph: Graph) -> None:
    """
    Handles ASIN selection and updates Tkinter interface based on selected ASIN.

    Preconditions:
    - type(root) == tk.Tk
    """
    selected_asin = str(asin_combobox.get())

    # ANALYSIS OF THIS PRODUCT
    # ratings
    this_products_reviews = graph.get_neighbouring_reviews(selected_asin)

    # sentiment analysis of this product
    sentiment_of_reviews = []
    for review in this_products_reviews:
        sentiment_of_reviews.append(sentiment_analysis(clean_text(review.review_text)))

    # GET SIMILAR PRODUCTS
    # similar_products_and_reviews: dict[str asin of product: Review object]
    similar_products_and_reviews = graph.get_similar_product_reviews(selected_asin)

    most_similar_products = []
    all_review_text = ""  # string of all important words in all reviews for wordcloud
    for asin in similar_products_and_reviews:
        for review in similar_products_and_reviews[asin]:
            # clean the text using NLP
            cleaned_review_text = clean_text(review.review_text)
            all_review_text += cleaned_review_text + " "
            if sentiment_analysis(review.review_text)['compound'] >= 0.5:
                most_similar_products.append(asin)

    # this product subtitle
    subtitle = tk.Label(root, text="About this Product:", font=("Arial", 16, "bold"))
    subtitle.grid(row=3, column=1, padx=0, pady=(20, 10), sticky="w")

    # this product subtitle
    subtitle = tk.Label(root, text="Sentiment Distributions of More Recommended Products", font=("Arial", 16, "bold"))
    subtitle.grid(row=3, column=3, padx=0, pady=(20, 10), sticky="w")

    # scatter plot
    scatter_plot_fig = generate_scatter_plot_figure(this_products_reviews)
    display_figure(scatter_plot_fig, root, (4, 1))

    # this product pie chart
    sentiment_fig = plot_sentiment_analysis_current_product(sentiment_of_reviews, selected_asin)
    display_figure(sentiment_fig, root, (4, 2))

    # other products subtitle
    subtitle = tk.Label(root, text="Other Products You'd Like:", font=("Arial", 16, "bold"))
    subtitle.grid(row=5, column=1, padx=10, pady=(20, 10), sticky="w")

    # recommended products
    similar_products_listbox = tk.Listbox(root, height=10, width=5)
    similar_products_listbox.grid(row=6, column=1, padx=10, pady=10, sticky="we")
    similar_products_listbox.delete(0, tk.END)  # clear existing entries
    for asin in most_similar_products[:6]:
        similar_products_listbox.insert(tk.END, asin)

    # wordcloud
    wordcloud_fig = generate_wordcloud_figure(all_review_text)
    display_figure(wordcloud_fig, root, (6, 2))

    # scatter plot and pie chart for sentiment analysis of similar product reviews
    avg_sentiment_fig = plot_average_sentiment_analysis_score(similar_products_and_reviews, selected_asin)
    display_figure(avg_sentiment_fig, root, (6, 3))

    sentiment_dist_fig = plot_sentiment_distribution(similar_products_and_reviews)
    display_figure(sentiment_dist_fig, root, (4, 3))
