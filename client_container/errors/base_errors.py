class BaseError(Exception):
    @property
    def status_code(self):
        raise NotImplementedError

    @property
    def description(self):
        raise NotImplementedError


class BadRequestError(BaseError):
    status_code = 400
    title = "Bad Request"
    description = "The requested could not be processed!"


class NotFoundError(BaseError):
    status_code = 404
    title = "Not Found"
    description = "The requested resource could not be found!"


class InternalServerError(BaseError):
    status_code = 500
    title = "Internal Server Error"
    description = "The requested could not be processed!"
