from flask import jsonify
from flask.views import MethodView

from controllers import RecordController


class Record(MethodView):
    def __init__(self, context):
        self.record_controller = RecordController(context)

    def get(self, month: int):
        result = self.record_controller.get_by_month(month)

        return result
