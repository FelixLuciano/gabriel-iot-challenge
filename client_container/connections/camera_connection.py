from connections.http_connection import HttpConnection
from constants import CAMERA_SERVICE_URL
from errors import NotFoundError, InternalServerError


class CameraConnection(HttpConnection):
    BASE_URL = CAMERA_SERVICE_URL

    def fetch_month(self, month: int):
        response = self.send(f"/month/{month}", "GET")

        if response.status_code == 404:
            raise NotFoundError
        elif response.status_code != 200:
            raise InternalServerError

        data = response.json()

        if data.get("result", None) != "success":
            raise InternalServerError

        return data.get("data")

    def fetch_day(self, day: int, month: int):
        response = self.send(f"/month/{month}/day/{day}", "GET")

        if response.status_code == 404:
            raise NotFoundError
        elif response.status_code != 200:
            raise InternalServerError
        
        data = response.json()

        if data.get("result", None) != "success":
            raise InternalServerError

        return data.get("data")
