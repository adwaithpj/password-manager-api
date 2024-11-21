from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from configs.Environment import get_environment_variables

env = get_environment_variables()


# DATABASE_URL = f"sqlite:///./passman.db"
DATABASE_URL = f"{env.DATABASE_DIALECT}://{env.DATABASE_USERNAME}:{env.DATABASE_PASSWORD}@{env.DATABASE_HOSTNAME}/{env.DATABASE_NAME}?sslmode=require"

Engine = create_engine(
    DATABASE_URL,
    connect_args={"connect_timeout": 50},
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)


def get_db_connection():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()
