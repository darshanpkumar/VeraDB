from dataclasses import dataclass


@dataclass
class VectorItem:
    """
    Represents a single vector stored in VeraDB.
    """

    id: int
    vector: list[float]
    metadata: dict | None = None