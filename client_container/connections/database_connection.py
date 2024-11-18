from contextlib import contextmanager

from flask import Flask
from sqlalchemy.orm import Session


class DatabaseConnection:
    SESSION_CONFIG = {
        "expire_on_commit": False,
    }

    def __init__(self, context: Flask):
        self.context = context

    @contextmanager
    def get_session(self):
        try:
            with Session(self.context.db, **DatabaseConnection.SESSION_CONFIG) as session:
                yield session
        except Exception as error:
            self.context.logger.fatal(error, error.args)
            session.rollback()
        finally:
            session.close()
