import logging

from flask import Flask, g, jsonify
from sqlalchemy import create_engine, text

from connections import DatabaseConnection
from constants import DB_SERVICE_URL
from errors import BaseError
from models import BaseModel, DiscEventModel, RecordTypeModel
from resources import Record


# logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#     datefmt='%Y-%m-%d:%H:%M:%S',
#     level=logging.DEBUG)

app = Flask(__name__)

app.db = create_engine(DB_SERVICE_URL, echo=True)

app.add_url_rule("/record/<int:month>", view_func=Record.as_view("record", app))

@app.errorhandler(404)
def not_found(error):
    response ={
        "message": error.description,
    }

    app.logger.error(f"ERROR: {error.description}")

    return jsonify(response), 404

@app.errorhandler(BaseError)
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
    BaseModel.metadata.create_all(app.db)

    models = [
        DiscEventModel.create(0, "EVENT0"),
        DiscEventModel.create(1, "EVENT1"),
        DiscEventModel.create(2, "EVENT2"),
        DiscEventModel.create(4, "EVENT4"),
        RecordTypeModel.create(1, "NormalRecord"),
        RecordTypeModel.create(2, "AlarmRecord"),
        RecordTypeModel.create(4, "MotionRecord"),
    ]

    with DatabaseConnection(app).get_session() as session:
        session.add_all(models)
        session.commit()

    # app.db.raw_connection().cursor().executescript(open("schema.sql").read())

init_db()

if __name__ == "__main__":
    app.run(debug=True)
