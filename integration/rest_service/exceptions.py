class ServiceUnavailableException(Exception):
    pass


class ImproperlyConfigured(Exception):
    pass


class HandledSatelliteException(Exception):
    status_code = 400
    error_code = ""


class UnusableMembership(HandledSatelliteException):
    # Valid membership but deleted, expired, canceled, etc
    error_code = "UNUSABLE_MEMBERSHIP"


class InvalidMembership(HandledSatelliteException):
    # Not existent membership
    error_code = "INVALID_MEMBERSHIP"


class BadRequest(HandledSatelliteException):
    error_code = "BAD_REQUEST"


class SearchFilterLimitReached(BadRequest):
    error_code = "SEARCH_FILTER_LIMIT_REACHED"


class NotFound(HandledSatelliteException):
    status_code = 404
    error_code = "NOT_FOUND"
