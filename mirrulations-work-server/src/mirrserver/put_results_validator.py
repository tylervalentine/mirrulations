from flask import json, request

class NoResultsException(Exception):
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
    def check_put_results(self, data):
        data = json.loads(request.get_json())
        if data is None or data.get('results') is None:
            raise NoResultsException()
        client_id = request.args.get('client_id')
        if client_id is None:
            raise InvalidClientIDException()
        if isinstance(client_id, int) and client_id < 20 and client_id >= 0:
            return True