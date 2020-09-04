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
