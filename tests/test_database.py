# ---
# created: 13 Apr 2026
# author: kaedonkers
# modified: 14 Apr 2026
# ---
# Test database

import os
import tempfile
import sqlalchemy as sqla
import sqlalchemy.orm

from app import database, models

def test_database_connection(test_engine):
    # Connect to test database
    with test_engine.connect() as conn:
        # Execute simple query
        result = conn.execute(sqla.text("SELECT 1"))
        assert result.scalar() == 1

def test_tables_can_be_created(test_engine):
    # Create tables
    database.BaseDB.metadata.create_all(bind=test_engine)
    # Verify `todos` table exists
    assert "todos" in sqla.inspect(test_engine).get_table_names()

def test_db_disk_persistence(test_session, test_db_path):
    # Add record to test database fixture
    todo = models.Todo(
        title="test_db_disk_persistence", 
        description="Testing disk persistence of the database.",
        )
    test_session.add(todo)
    # Get the record ID to verify persistence later
    test_session.flush()
    todo_id = todo.id
    assert todo_id is not None
    # Commit to test database
    test_session.commit()
    # Start new session to verify record has persisted in test database
    try:
        assert os.path.exists(test_db_path)
        engine2 = sqla.create_engine(f"sqlite:///{test_db_path}")
        Session2 = sqla.orm.sessionmaker(bind=engine2)
        db_session2 = Session2()
        try:
            persisted = db_session2.get(models.Todo, todo_id)
            assert persisted is not None
            assert persisted.id == todo_id
            assert persisted.title == "test_db_disk_persistence"
            assert persisted.description == "Testing disk persistence of the database."
        finally:
            # Remove test record
            db_session2.delete(persisted)
            db_session2.commit()
            # Close second session
            db_session2.close()
    finally: 
        # Dispose of second engine
        engine2.dispose()

