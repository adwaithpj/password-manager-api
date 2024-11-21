from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# DATABASE_URL = f"sqlite:///./passman.db"
DATABASE_URL = "postgresql://passmandb_user:kVu4TCpOfVRDQNsCpW13mxf4qmF4GmLY@dpg-csvfnkdumphs7385533g-a.singapore-postgres.render.com/passmandb?sslmode=require"

Engine = create_engine(
    DATABASE_URL,
    connect_args={"connect_timeout": 10},
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)


def get_db_connection():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()
