
class UserCredentialsExhaustedException(Exception):
    """
    Raised when user's have exhausted in user pool
    """
    pass


class LoginFailureException(Exception):
    """
    Failed to perform login
    """
    pass
