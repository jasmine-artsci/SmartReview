from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def clean_text(text: str) -> str:
    """
    Removes unneeded words like "the", "and", "I", etc., and returns a string cleaned of these unneeded words.
    Tokenizes the text into sentences and then words using nltk.tokenize,
    filters out stopwords using nltk.corpus.stopwords.

    Preconditions:
    - set(stopwords.words('english')) != set()
    """
    stop_words = set(stopwords.words('english'))
    punctuation = [
        "!", "\"", "#", "$", "%", "&", "'", "(", ")",
        "*", ",", "-", ".", "/", ":", ";", "<",
        "=", ">", "?", "@", "[", "]", "^", "_",
        "`", "{", "|", "}", "~"
    ]

    # tokenize into words
    tokens = word_tokenize(text)

    # filter out stop words
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words and token not in punctuation]

    cleaned_text = '  '.join(filtered_tokens)

    return cleaned_text


def sentiment_analysis(text: str) -> dict:
    """
    Return a dictionary of the negative, neutral, and positive score distribution of each individual review.
    Preconditions:
    - negative score + neutral score + positive score = 1
    - negative score + neutral score + positive score > 0
    - -1 <= compound score <= 1
    """
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(clean_text(text))


def average_sentiment_analysis(similar_product_review: dict[str, list[str]]) -> dict[str, float]:
    """
    Return a dictionary of average compound sentiment scores of the reviews for each similar product.
    The compound value represents the overal sentiment of a text and ranges from -1 to 1.
    If compound score >= 0.05, the statement has a positive sentiment.
    If compound score <= -0.05, the statement has a negative sentiment.
    If -0.05 < compound score < 0.05, the statement has a neutral sentiment.

    Preconditions:
    - negative score + neutral score + positive score = 1
    - negative score + neutral score + positive score > 0
    - -1 < compound score < 1
    """
    sentiment_scores = {}
    for asin, reviews in similar_product_review.items():
        total = 0
        for r in reviews:
            total += sentiment_analysis(clean_text(r.review_text))['compound']
        average = total / len(reviews)
        sentiment_scores[asin] = average
    return sentiment_scores


def sentiment_dist_analysis(similar_product_review: dict[str, list[str]]) -> dict:
    """
    Analyze the sentiment distribution by calculating the ratio of positive to negative sentiment scores.

    Preconditions:
    - negative score + neutral score + positive score = 1
    - negative score + neutral score + positive score > 0
    - -1 < compound score < 1
    """
    sentiment_scores = {}
    for asin, reviews in similar_product_review.items():
        total_positive = 0
        total_negative = 0
        for r in reviews:
            scores = sentiment_analysis(clean_text(r.review_text))
            total_positive += scores['pos']
            total_negative += scores['neg']
        sentiment_scores[asin] = {'Positive': total_positive, 'Negative': total_negative}
    return sentiment_scores
