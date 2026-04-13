# ---
# created: 13 Apr 2026
# author: kaedonkers
# modified: 13 Apr 2026
# ---
# Database setup and session management

import sqlalchemy as sqla
import sqlalchemy.orm

SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

engine = sqla.create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sqla.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseDB = sqla.orm.declarative_base()

def get_db():
    '''
    Provides a database session to the API endpoints
    using a pseudo-context manager pattern to ensure proper cleanup
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
