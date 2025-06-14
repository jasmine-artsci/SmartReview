from typing import Any
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from wordcloud import WordCloud
import pandas as pd
from review import Review
from text_analysis import average_sentiment_analysis, sentiment_dist_analysis


def plot_sentiment_analysis_current_product(sentiment_results: list[dict[str, float]], main_asin: str) -> Figure:
    """
    Plot the sentiment analysis results for the current product.

    Preconditions:
    - len(sentiment_results) > 0
    """
    negative = sum(result['neg'] for result in sentiment_results)
    neutral = sum(result['neu'] for result in sentiment_results)
    positive = sum(result['pos'] for result in sentiment_results)

    sentiment = ['Negative', 'Neutral', 'Positive']
    scores = [negative, neutral, positive]

    fig = Figure(figsize=(4, 2))
    ax = fig.add_subplot(111)
    ax.pie(scores, labels=sentiment, autopct=lambda pct: ('%1.1f%%' % pct) if pct > 0 else '', startangle=90)
    ax.set_title(f'Sentiment of Reviews for {main_asin}', fontsize=8)

    return fig


def plot_average_sentiment_analysis_score(similar_product_reviews: dict, main_asin: str) -> Figure:
    """
    Plot the average sentimental analysis score for reviews of each ASIN. The function takes in a dictionary, which has
    product ASIN as keys and average sentimental score as values, and plots the average for each similar product.

    Preconditions:
    - len(similar_product_reviews) != 0
    """
    sentiment_scores = average_sentiment_analysis(similar_product_reviews)
    asins = list(sentiment_scores.keys())
    averages = list(sentiment_scores.values())

    fig = Figure(figsize=(4, 2))
    ax = fig.add_subplot(111)
    ax.scatter(asins, averages, alpha=0.5)
    ax.set_title(f'Average Sentiment for Products Similar to {main_asin}', fontsize=7)
    ax.set_xlabel('Product ASIN', fontsize=6)
    ax.set_ylabel('Average Sentiment Score', fontsize=6)
    ax.tick_params(axis='x', rotation=45, labelsize=5)
    fig.tight_layout()

    return fig


def plot_sentiment_distribution(similar_product_reviews: dict) -> Figure:
    """
    Plot the sentiment distribution by calculating the ratio of positive to negative sentiment scores.

    Preconditions:
    - len(similar_product_reviews) != 0
    """

    sentiment_distribution = sentiment_dist_analysis(similar_product_reviews)

    # calculate rows for subplots
    if len(sentiment_distribution) > 6:
        num_items = 6
    else:
        num_items = len(sentiment_distribution)
    num_columns = 2
    num_rows = (num_items + num_columns - 1) // num_columns

    fig = Figure(figsize=(4, 3))

    for i, (asins, scores) in enumerate(sentiment_distribution.items(), start=1):
        if i > 6:
            break
        # subplots for each pie chart
        ax = fig.add_subplot(num_rows, num_columns, i)

        analysis = list(scores.keys())
        counts = list(scores.values())
        # ensure there are no NaN values that could cause an error
        counts = [0 if not x else x for x in counts]

        ax.pie(counts, labels=analysis, autopct=lambda p: '{:.1f}%'.format(p) if p > 0 else '', startangle=90,
               textprops={'fontsize': 5})
        ax.set_title(f'ASIN: {asins}', fontsize=8)
        ax.axis('equal')

    fig.tight_layout(pad=2.0)

    return fig


def generate_wordcloud_figure(all_review_text: str) -> Figure:
    """
    Returns a matplotlib Figure with a word cloud of common words in the review text provided.

    Preconditions:
    - len(all_review_text) > 0
    """
    if all_review_text == "":
        raise ValueError
    wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(all_review_text)
    fig = Figure(figsize=(3, 2))
    ax = fig.add_subplot(111)
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis('off')
    fig.suptitle("Reviews of Recommended Products", fontsize=7, fontweight='bold')
    return fig


def generate_scatter_plot_figure(product_reviews: set[Review]) -> Figure:
    """
    Returns a matplotlib Figure displaying a scatter plot of product ratings with respect to the date they were rated.

    Preconditions:
    - product_reviews != set()
    - all([type(r) == Review for r in product_reviews])
    """
    review_data = [{'review_time': r.review_time, 'rating': r.rating} for r in product_reviews]
    df = pd.DataFrame(review_data)
    df['review_time'] = pd.to_datetime(df['review_time'])
    df.sort_values('review_time', inplace=True)

    fig = Figure(figsize=(4, 2))
    ax = fig.add_subplot(111)
    ax.scatter(df['review_time'], df['rating'], alpha=0.5)
    ax.set_title("Product Ratings Over Time", fontsize=7)
    ax.set_xlabel('Review Time', fontsize=6)
    ax.set_ylabel('Rating', fontsize=6)
    ax.tick_params(axis='x', rotation=45, labelsize=5)
    fig.tight_layout()
    return fig


def display_figure(fig: Figure, root: Any, position: tuple[int]) -> None:
    """
    Displays a matplotlib figure in a specified grid position in the Tkinter window.

    Preconditions:
    - position[0] > 0
    - position[1] > 0
    """
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.grid(row=position[0], column=position[1], padx=10, pady=10)
