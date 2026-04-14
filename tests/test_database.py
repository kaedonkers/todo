# ---
# created: 13 Apr 2026
# author: kaedonkers
# modified: 13 Apr 2026
# ---

import sqlalchemy as sqla
import sqlalchemy.orm

from app.database import engine, SessionLocal, BaseDB, get_db

GENERATOR_TYPE = type((lambda: (yield))())

def test_engine_type():
    assert isinstance(engine, sqla.engine.base.Engine)

def test_sessionlocal_type():
    assert isinstance(SessionLocal, sqla.orm.session.sessionmaker)

def test_basedb_type():
    assert isinstance(BaseDB, sqla.orm.decl_api.DeclarativeMeta)

def test_get_db_types():
    # Check database generator
    db_gen = get_db()
    assert isinstance(db_gen, GENERATOR_TYPE)

    # Check yielded session
    db = next(db_gen)
    assert isinstance(db, sqla.orm.session.Session)

