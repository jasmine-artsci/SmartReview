from __future__ import annotations
from typing import Any


class Vertex:
    """A vertex in a graph.

    Instance Attributes:
        - item: The data stored in this vertex (ASIN or reviewerID).
        - kind: The type of vertex it is, either 'product' or 'reviewer'.
        - neighbours: The vertices that are adjacent to this vertex.
    """
    item: Any
    kind: str
    neighbours: dict[Vertex, Any]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.kind = kind
        self.neighbours = {}
