class TokenError(Exception):
    """
    error : -
    """
    def __str__(self):
        return "Token is not valid"
