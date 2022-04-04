class InvalidResultsException(Exception):
    """
    Raised when no results/json data are sent
    """
    pass


class InvalidClientIDException(Exception):
    """
    Raised when the client ID is invalid
    (not 0<=client_id<20 or not an integer)
    """
    pass


class PutResultsValidator():
    """Validates the results sent by the client"""
    def check_put_results(self, data, client_id):
        if data is None or data.get('results') is None:
            raise InvalidResultsException()
        if client_id is None:
            raise InvalidClientIDException()
        if not (isinstance(client_id, int) and client_id < 20 and client_id >= 0):
            raise InvalidClientIDException()
        else:
            return True
