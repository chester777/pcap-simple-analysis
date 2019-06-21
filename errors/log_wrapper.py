class ParamError(Exception) :

    def __str__(self):
        return "One of these three arguments must be true : db, file or display"
