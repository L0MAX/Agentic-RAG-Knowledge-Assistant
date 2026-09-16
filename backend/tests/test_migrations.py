from sqlalchemy import inspect, text
from tests.db_support import REQUIRED_TABLES, requires_postgres


@requires_postgres
def test_migrations_create_expected_schema(test_engine) -> None:
    inspector = inspect(test_engine)
    tables = set(inspector.get_table_names())
    assert REQUIRED_TABLES.issubset(tables)

    with test_engine.connect() as connection:
        extension = connection.execute(
            text("SELECT extname FROM pg_extension WHERE extname = 'vector'")
        ).scalar_one()
        assert extension == "vector"
        indexes = connection.execute(
            text(
                """
                SELECT indexname
                FROM pg_indexes
                WHERE tablename = 'document_chunks'
                  AND indexname = 'ix_document_chunks_embedding_hnsw'
                """
            )
        ).scalar_one()
        assert indexes == "ix_document_chunks_embedding_hnsw"

    user_fks = {fk["referred_table"] for fk in inspector.get_foreign_keys("knowledge_bases")}
    assert "users" in user_fks
    chunk_fks = {fk["referred_table"] for fk in inspector.get_foreign_keys("document_chunks")}
    assert "documents" in chunk_fks
