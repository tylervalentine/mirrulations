from mirrclient.exceptions import InvalidResultsException
from mirrclient.exceptions import InvalidClientIDException
from mirrclient.exceptions import MissingClientIDException


class PutResultsValidator():
    """Validates the results sent by the client"""
    @classmethod
    def check_put_results(cls, data, client_id):
        if data is None or data.get('results') is None:
            raise InvalidResultsException()
        if client_id is None:
            raise MissingClientIDException()
        if client_id.isdigit() or isinstance(client_id, int):
            client_id = int(client_id)
            if 0 < client_id:
                return {'success': 'Job was successfully completed'}, 200
        raise InvalidClientIDException()
