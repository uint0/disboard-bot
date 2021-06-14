class ServerForbiddenException(Exception):
    """ Raised when no the requester does not have perms """

class ServerNotConfiguredException(Exception):
    """ Raised when a server cannot be found in config """