from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from configs.Environment import get_environment_variables
from sqlalchemy.exc import OperationalError
from time import sleep

env = get_environment_variables()


# DATABASE_URL = f"sqlite:///./passman.db"
DATABASE_URL = f"{env.DATABASE_DIALECT}://{env.DATABASE_USERNAME}:{env.DATABASE_PASSWORD}@{env.DATABASE_HOSTNAME}:{env.DATABASE_PORT}/{env.DATABASE_NAME}?sslmode=require"

# Engine = create_engine(
#     DATABASE_URL,
#     connect_args={"connect_timeout": 50},
#     future=True,
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)


# def get_db_connection():
#     db = scoped_session(SessionLocal)
#     try:
#         yield db
#     finally:
#         db.close()
MAX_RETRIES = 3
for attempt in range(MAX_RETRIES):
    try:
        Engine = create_engine(
            DATABASE_URL,
            connect_args={"connect_timeout": 50},
            pool_pre_ping=True,  # Ensures broken connections are detected
            future=True,
        )
        break
    except OperationalError as e:
        if attempt < MAX_RETRIES - 1:
            print(
                f"Database connection failed. Retrying... ({attempt + 1}/{MAX_RETRIES})"
            )
            sleep(2)  # Wait before retrying
        else:
            raise RuntimeError(
                "Failed to connect to the database after multiple retries."
            ) from e

# Configure session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)


def get_db_connection():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Error during database session: {e}")
        raise
    finally:
        db.close()
