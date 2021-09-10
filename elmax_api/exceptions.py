"""Exceptions for the Elmax Cloud services client."""


class ElmaxError(Exception):
    """General ElmaxError exception occurred."""

    pass


class ElmaxApiError(Exception):
    """Occurs when an API returns an unexpected return code"""

    def __init__(self, status_code: int):
        self._status_code = status_code

    @property
    def status_code(self):
        return self._status_code


class ElmaxNetworkError(ElmaxError):
    """When a network error is encountered."""

    pass


class ElmaxBadLoginError(ElmaxError):
    """Occurs when a login attempt fails"""

    pass
