from contextlib import contextmanager

from flask_restx import Api
from sqlalchemy.orm import Session


class DatabaseConnection:
    SESSION_CONFIG = {
        "expire_on_commit": False,
    }

    def __init__(self, context: Api):
        self.context = context

    @contextmanager
    def get_session(self):
        session = None

        try:
            with Session(self.context.db, **DatabaseConnection.SESSION_CONFIG) as session:
                yield session
        except Exception as error:
            self.context.logger.fatal(error, error.args)

            if session is not None:
                session.rollback()
        finally:
            if session is not None:
                session.close()
