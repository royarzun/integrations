class ServiceUnavailableException(Exception):
    status_code = 503


class ImproperlyConfigured(Exception):
    pass
