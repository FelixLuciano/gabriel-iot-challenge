# import logging

from flask import Flask, g, jsonify
from flask_restx import Api
from sqlalchemy import create_engine

from connections import DatabaseConnection
from constants import DB_SERVICE_URL
from errors import BaseError
from models import BaseModel, DiscEventModel, RecordTypeModel
from resources import Records


# logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#     datefmt='%Y-%m-%d:%H:%M:%S',
#     level=logging.DEBUG)

app = Flask(__name__)
api = Api(
    app=app,
    title='Gabriel IoT Challenge',
    version='0.0.1',
    doc="/docs",
)

api.db = create_engine(DB_SERVICE_URL, echo=False)

api.add_namespace(Records)

@api.errorhandler(BaseError)
def handle_exception(error: BaseError):
    response = {
        "status_code": error.status_code,
        "title": error.title,
        "description": error.description,
    }

    app.logger.error(f"{error.title}: {error.description}")

    return jsonify(response), error.status_code

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop("db", None)

    if db is None:
        return

    db.close()

def init_db():
    BaseModel.metadata.drop_all(api.db)
    BaseModel.metadata.create_all(api.db)

    models = [
        DiscEventModel.create(0, "EVENT0"),
        DiscEventModel.create(1, "EVENT1"),
        DiscEventModel.create(2, "EVENT2"),
        DiscEventModel.create(3, "EVENT3"),
        DiscEventModel.create(4, "EVENT4"),
        DiscEventModel.create(5, "EVENT5"),
        DiscEventModel.create(6, "EVENT6"),
        RecordTypeModel.create(1, "NormalRecord"),
        RecordTypeModel.create(2, "AlarmRecord"),
        RecordTypeModel.create(4, "MotionRecord"),
    ]

    with DatabaseConnection(api).get_session() as session:
        session.add_all(models)
        session.commit()

init_db()

if __name__ == "__main__":
    app.run(debug=True)
