from __future__ import annotations
from typing import Any
from vertex import Vertex
from review import Review


class Graph:
    """
    A graph used to represent an Amazon products review network.

    Instance Attributes:
        - vertices: a collection of the vertices contained in this graph, which maps item to Vertex objects
    """
    vertices: dict[Any, Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self.vertices = {}

    def add_vertex(self, item: Any, kind: str) -> None:
        """
        Mutates the vertices dictionary to add a Vertex object to the Graph.

        Preconditions:
        - kind in ['product','reviewer']
        """
        self.vertices[item] = Vertex(item, kind)

    def add_edge(self, item1: Any, item2: Any, review: Review) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
            - type(review) == Review
        """
        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            v2 = self.vertices[item2]

            v1.neighbours[v2] = review
            v2.neighbours[v1] = review
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_vertex(self, item: str) -> Vertex:
        """
        Returns the vertex associated with the given ASIN or ReviewerID.

        Preconditions:
        - item in self.vertices
        """
        return self.vertices[item]

    def get_similar_product_reviews(self, asin_of_interest: str) -> dict[str, list[Review]]:
        """
        Get products that are similar to the product with asin_of_interest.
        Returns dictionary mapping ASINs of the similar products to corresponding Reviews from shared reviewers.

        Preconditions:
        - asin_of_interest in self.vertices
        - len(self.vertices[asin_of_interest].neighbours) > 0
        """
        product_of_interest = self.get_vertex(asin_of_interest)
        similar_products = {}
        reviewers = [n for n in product_of_interest.neighbours.keys() if n.kind == 'reviewer']
        for reviewer in reviewers:
            other_products = [(n, reviewer.neighbours[n]) for n in reviewer.neighbours
                              if n.item != asin_of_interest]
            for product, review in other_products:
                # only consider those with ratings greater than 3 star
                if product.item in similar_products and review.rating > 3.0:
                    similar_products[product.item].append(review)
                elif product.item not in similar_products and review.rating > 3.0:
                    similar_products[product.item] = [review]
        return similar_products

    def get_neighbouring_reviews(self, item: Any) -> set[Review]:
        """Return a set of the Reviews stored in the edges of the given item.

        Note that the *Review objects* are returned (stored in the edges of the graph), not  Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.

        Preconditions:
        - item in self.vertices
        - len(self.vertices[item].neighbours) > 0
        """
        neighboring_reviews = set()
        if item in self.vertices:
            v = self.vertices[item]
            for n in v.neighbours:
                review = v.neighbours[n]
                neighboring_reviews.add(review)
            return neighboring_reviews
        else:
            raise ValueError
