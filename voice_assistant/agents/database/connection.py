import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


load_dotenv()


class DatabaseConnection:

    def __init__(self):
        self.host = os.getenv(
            "POSTGRES_HOST",
            "localhost"
        )

        self.port = os.getenv(
            "POSTGRES_PORT",
            "5432"
        )

        self.database = os.getenv(
            "POSTGRES_DB",
            "omnisupport"
        )

        self.username = os.getenv(
            "POSTGRES_USER",
            "postgres"
        )

        self.password = os.getenv(
            "POSTGRES_PASSWORD",
            ""
        )

        self.engine = None

    def get_connection_url(self):

        return (
            f"postgresql+psycopg2://"
            f"{self.username}:"
            f"{self.password}@"
            f"{self.host}:"
            f"{self.port}/"
            f"{self.database}"
        )

    def connect(self):

        if self.engine is not None:
            return self.engine

        try:

            self.engine = create_engine(
                self.get_connection_url(),
                pool_pre_ping=True,
                future=True,
            )

            # Test connection
            with self.engine.connect() as connection:
                connection.execute(
                    text("SELECT 1")
                )

            print(
                "PostgreSQL connection established."
            )

            return self.engine

        except SQLAlchemyError as e:

            self.engine = None

            raise ConnectionError(
                f"PostgreSQL connection failed: {e}"
            )

    def test_connection(self):

        try:

            engine = self.connect()

            with engine.connect() as connection:

                result = connection.execute(
                    text("SELECT 1")
                )

                return result.scalar() == 1

        except Exception as e:

            print(
                f"PostgreSQL test failed: {e}"
            )

            return False

    def close(self):

        if self.engine is not None:

            self.engine.dispose()

            self.engine = None

            print(
                "PostgreSQL connection closed."
            )