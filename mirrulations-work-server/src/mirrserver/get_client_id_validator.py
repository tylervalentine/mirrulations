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


class GetClientIDValidator():
    """Validates the results sent by the client"""
    def check_get_job_id(self, client_id):
        if client_id is None:
            client_id = '1'
            return True
        if client_id.isdigit() or isinstance(client_id, int):
            client_id = int(client_id)
            if (client_id < 20 and client_id > 0):
                return True
        raise InvalidClientIDException()
