from flask_restx import Api
from requests import request, Response
from requests.exceptions import JSONDecodeError


class HttpConnection:
    def __init__(self, context: Api):
        self.context = context

    @property
    def BASE_URL(self):
        raise NotImplementedError

    def send(self, endpoint: str, method: str) -> Response:
        url = self.BASE_URL + endpoint

        self.context.logger.debug(f"OUTGOING REQUEST TO {url}")

        response = request(
            method=method,
            url=url,
        )

        try:
            content = response.json()
        except JSONDecodeError:
            content = response.content

        self.context.logger.debug(f"INCOMING RESPONSE FROM {response.status_code} {url} - {content}")

        return response
