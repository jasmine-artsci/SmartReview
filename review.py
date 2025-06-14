class Review:
    """Review data that will be stored in edges.

    Instance Attributes:
        - rating: The rating given by the reviewer.
        - review_time: The time when the review was posted.
        - review_text: The text of the review.
    """
    rating: float
    review_time: str
    review_text: str

    def __init__(self, rating: float, review_time: str, review_text: str) -> None:
        """Initialize a new review object with the given data."""
        self.rating = rating
        self.review_time = review_time
        self.review_text = review_text
