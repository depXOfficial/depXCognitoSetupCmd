class InvalidCSVFormat(Exception):
    "Raised when credentials csv file is not in the right format"
    pass

class InvalidCredentialsError(Exception):
    "Raised when credentials are invalid"
    pass