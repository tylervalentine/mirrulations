from mirrserver.exceptions import InvalidResultsException
from mirrserver.exceptions import InvalidClientIDException
from mirrserver.exceptions import MissingClientIDException


class PutResultsValidator():
    """Validates the results sent by the client"""
    def check_put_results(self, data, client_id):
        if data is None or data.get('results') is None:
            raise InvalidResultsException()
        if client_id is None:
            raise MissingClientIDException()
        if client_id.isdigit() or isinstance(client_id, int):
            client_id = int(client_id)
            if 0 < client_id < 21:
                return {'success': 'Job was successfully completed'}, 200
        raise InvalidClientIDException()
