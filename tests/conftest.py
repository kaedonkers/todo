# ---
# created: 14 Apr 2026
# author: kaedonkers
# modified: 14 Apr 2026
# ---
# Setup for testing, including:
# - Temporary, on-disk database (isolation, no side-effects)
# - Test client that uses temporary database

import os
import tempfile

import pytest
import sqlalchemy as sqla
import sqlalchemy.orm
from fastapi.testclient import TestClient

from app import database, main

@pytest.fixture(scope="function")
def test_db_path():
    '''
    Creates temporary file to be used as database for testing
    '''
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    try:
        yield db_path
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)

@pytest.fixture(scope="function")
def test_engine(test_db_path):
    '''
    Create engine connected to temporary database file
    '''
    engine = sqla.create_engine(
        f"sqlite:///{test_db_path}",
        connect_args={"check_same_thread": False},
    )
    try:
        yield engine
    finally:
        engine.dispose()

@pytest.fixture(scope="function")
def test_session(test_engine):
    '''
    Start session connected to temporary database
    '''
    # Start session
    TestingSessionLocal = sqla.orm.sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )
    # Create tables
    database.BaseDB.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        # Cleanup
        session.close()
        database.BaseDB.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def test_client(test_session):
    '''
    Provides a TestClient that uses temporary database
    '''
    # Override default get_db in API
    def _override_get_db():
        try:
            yield test_session
        finally:
            pass
    main.app.dependency_overrides[database.get_db] = _override_get_db
    # Yield test client
    with TestClient(main.app) as c:
        yield c
    main.app.dependency_overrides.clear()

# Probably not necessary, but here if needed
@pytest.fixture(scope="function")
def real_client():
    '''
    Provides a TestClient that uses the actual app database for testing
    '''
    with TestClient(main.app) as c:
        yield c
