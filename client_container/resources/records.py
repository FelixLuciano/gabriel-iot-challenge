import datetime

from flask import request
from flask.views import MethodView

from controllers import RecordController
from utils.schema_handler import SchemaHandler


class Records(MethodView):
    query_validator = SchemaHandler("./schema/GET_Records_query.json")

    def __init__(self, context):
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

    def get_by_query(self):
        params = dict(request.args)

        Records.query_validator.validate(params)

        if "reference_date" in params:
            reference_date = datetime.date.fromisoformat(params["reference_date"])
            records = self.record_controller.get_by_date(reference_date)
        
        elif "reference_start" in params and "reference_end" in params:
            reference_start = datetime.datetime.fromisoformat(params["reference_start"])
            reference_end = datetime.datetime.fromisoformat(params["reference_end"])
            records = self.record_controller.get_by_period(reference_start, reference_end)

        return records
