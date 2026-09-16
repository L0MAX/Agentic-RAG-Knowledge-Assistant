"""Shared database column constants.

Embedding dimensions are fixed at migration time. Changing EMBEDDING_DIMENSIONS
in the environment requires a new Alembic revision.
"""

EMBEDDING_DIMENSIONS = 1536
