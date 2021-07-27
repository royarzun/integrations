class GenericSatelliteException(Exception):
    status_code = 500
    error_code = ""


class ServiceUnavailableException(Exception):
    status_code = 503


class ImproperlyConfigured(Exception):
    pass


class UnusableMembership(Exception):
    # Valid membership but deleted, expired, canceled, etc
    pass


class InvalidMembership(Exception):
    # Not existent membership
    pass


class BadRequest(GenericSatelliteException):
    status_code = 400
    error_code = "BAD_REQUEST"


class SearchFilterLimitReached(BadRequest):
    error_code = "SEARCH_FILTER_LIMIT_REACHED"


class NotFound(GenericSatelliteException):
    status_code = 404
    error_code = "NOT_FOUND"
