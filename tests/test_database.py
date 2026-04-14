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

# NB: Could use in-memory database for speed, but overkill for this demo project

def test_database_connection():
    with database.engine.connect() as conn:
        result = conn.execute(sqla.text("SELECT 1"))
        assert result.scalar() == 1

def test_tables_can_be_created():
    # Create tables
    database.BaseDB.metadata.create_all(bind=database.engine)
    # Verify `todos` table exists
    inspector = sqla.inspect(database.engine)
    assert "todos" in inspector.get_table_names()
    # Cleanup
    database.BaseDB.metadata.drop_all(bind=database.engine)

def test_db_disk_persistence():
    # Create a temporary filepath
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        # Create DB at the temp filepath
        engine = sqla.create_engine(f"sqlite:///{db_path}")
        database.BaseDB.metadata.create_all(bind=engine)
        # Verify file exists after creation
        assert os.path.exists(db_path)
        # Write data
        Session = sqla.orm.sessionmaker(bind=engine)
        db = Session()
        db.add(models.Todo(
            title="test_db_disk_persistence", 
            description="Testing disk persistence of the database.",
            ))
        db.commit()
        db.close()
        # Verify file exists after close
        assert os.path.exists(db_path)
        # Re-open and verify data has persisted
        engine2 = sqla.create_engine(f"sqlite:///{db_path}")
        Session2 = sqla.orm.sessionmaker(bind=engine2)
        db2 = Session2()
        count = db2.query(models.Todo).count()
        assert count == 1
        title = db2.query(models.Todo).first().title
        assert title == "test_db_disk_persistence"
        db2.close()
    # Cleanup
    finally: 
        # Just in case, ensure the file is removed after the test
        if os.path.exists(db_path): os.remove(db_path)
