from contextlib import contextmanager

from flask import Flask
from sqlalchemy.orm import Session


class DatabaseConnection:
    def __init__(self, context: Flask):
        self.context = context

    @contextmanager
    def get_session(self):
        try:
            with Session(self.context.db) as session:
                yield session
        except Exception as error:
            self.context.logger.fatal(error)
            session.rollback()
