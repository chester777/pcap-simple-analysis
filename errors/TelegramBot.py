class TokenError(Exception):

    def __str__(self):
        return "Token is not valid"
