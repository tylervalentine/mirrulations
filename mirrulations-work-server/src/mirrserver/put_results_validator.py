class InvalidResultsException(Exception):
    """
    Raised when no results/json data are sent
    """
    message = {'error': 'The body does not contain the results'}
    status_code = 403


class InvalidClientIDException(Exception):
    """
    Raised when the client ID is invalid
    (not 0<=client_id<20 or not an integer)
    """
    message = {'error': 'Invalid client ID'}
    status_code = 401


class MissingClientIDException(Exception):
    """
    Raised when the client ID is missing
    """
    message = {'error': 'Client ID was not provided'}
    status_code = 401


class PutResultsValidator():
    """Validates the results sent by the client"""
    def check_put_results(self, data, client_id):
        if data is None or data.get('results') is None:
            raise InvalidResultsException()
        if client_id is None:
            raise MissingClientIDException()
        if client_id.isdigit() or isinstance(client_id, int):
            client_id = int(client_id)
            if (client_id < 20 and client_id > 0):
                 return {'success': 'Job was successfully completed'},200
        raise InvalidClientIDException()