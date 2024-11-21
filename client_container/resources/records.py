import datetime

from flask import request
from flask_restx import Api, Namespace, Resource

from controllers import RecordController
from errors.base_errors import BadRequestError
from utils.schema_handler import SchemaHandler


class RecordsPath(Resource):
    def __init__(self, context: Api):
        self.context = context
        self.record_controller = RecordController(context)

    def get(self, year: int, month: int = None, day: int = None):
        if month is not None:
            if day is not None:
                records = self.record_controller.get_by_day(year, month, day)
            else:
                records = self.record_controller.get_by_month(year, month)
        else:
            records = self.record_controller.get_by_year(year)

        return records

class RecordsQuery(Resource):
    query_validator = SchemaHandler("./schema/GET_Records_query.json")

    def __init__(self, context: Api):
        self.context = context
        self.record_controller = RecordController(context)

    def get(self):
        params = dict(request.args)

        RecordsQuery.query_validator.validate(params)

        if "reference_date" in params:
            reference_date = datetime.date.fromisoformat(params["reference_date"])
            records = self.record_controller.get_by_date(reference_date)
        
        elif "reference_start" in params and "reference_end" in params:
            try:
                reference_start = datetime.datetime.fromisoformat(params["reference_start"])
                reference_end = datetime.datetime.fromisoformat(params["reference_end"])
            except ValueError as error:
                error_ = BadRequestError

                error_.description = "\n".join(error.args)

                raise error_

            records = self.record_controller.get_by_period(reference_start, reference_end)

        return records


Records = Namespace("records", description="Read event records from the camera")

Records.add_resource(RecordsQuery, "/", "/")
Records.add_resource(RecordsPath, "/", "/year/<int:year>")
Records.add_resource(RecordsPath, "/", "/year/<int:year>/month/<int:month>")
Records.add_resource(RecordsPath, "/", "/year/<int:year>month/<int:month>/day/<int:day>")
