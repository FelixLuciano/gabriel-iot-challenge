# import logging

from flask import Flask, g, jsonify
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

app.db = create_engine(DB_SERVICE_URL, echo=False)

records_resource = Records(app)

app.add_url_rule("/records/", view_func=records_resource.get_by_query, methods=["GET"])
app.add_url_rule("/records/year/<int:year>", view_func=Records.as_view("RecordsOnYear", app))
app.add_url_rule("/records/year/<int:year>/month/<int:month>", view_func=Records.as_view("RecordsOnMonth", app))
app.add_url_rule("/records/year/<int:year>/month/<int:month>/day/<int:day>", view_func=Records.as_view("RecordsOnDay", app))

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
    BaseModel.metadata.drop_all(app.db)
    BaseModel.metadata.create_all(app.db)

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

    with DatabaseConnection(app).get_session() as session:
        session.add_all(models)
        session.commit()

init_db()

if __name__ == "__main__":
    app.run(debug=True)
