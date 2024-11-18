import json

from jsonschema import validate, FormatChecker
from jsonschema.exceptions import ValidationError

from errors import BadRequestError


class SchemaHandler:
    def __init__(self, schema_path: str):
        self.schema_path = schema_path

        with open(schema_path, "r") as f:
            self.schema = json.load(f)

    def validate(self, instance: object):
        try:
            validate(instance, self.schema, format_checker=FormatChecker())
        except ValidationError as error:
            new_error = BadRequestError()

            new_error.description = error.message

            raise new_error
