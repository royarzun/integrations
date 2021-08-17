class ServiceUnavailableException(Exception):
    """
    Handle service unavailable or any other exception. Unhandled exception.
    """

    pass


class ImproperlyConfigured(Exception):
    """
    Handle error for improperly configuration from requester. Unhandled exception.
    """

    pass


class HandledSatelliteException(Exception):
    """
    Base class for Handled exceptions, these exceptions
    will response with the defined status code and the serialized error code.
    """

    status_code = 400
    error_code = ""


class UnusableMembership(HandledSatelliteException):
    """
    Handle valid membership but deleted, expired, canceled, etc.
    """

    error_code = "UNUSABLE_MEMBERSHIP"


class InvalidMembership(HandledSatelliteException):
    """
    Handle not existent membership.
    """

    error_code = "INVALID_MEMBERSHIP"


class BadRequest(HandledSatelliteException):
    """
    Handle Bad request.
    """

    error_code = "BAD_REQUEST"


class SearchFilterLimitReached(BadRequest):
    """
    Handle max allowed limit for search filter.
    """

    error_code = "SEARCH_FILTER_LIMIT_REACHED"


class NotFound(HandledSatelliteException):
    """
    Handle not found error.
    """

    status_code = 404
    error_code = "NOT_FOUND"
