from mirrserver.exceptions import InvalidClientIDException


class GetClientIDValidator():
    """Validates the client_id sent by the client"""
    @classmethod
    def check_get_client_id(cls, client_id):
        if client_id is None:
            client_id = '1'
            return True
        if client_id.isdigit() or isinstance(client_id, int):
            client_id = int(client_id)
            if 0 < client_id:
                return True
        raise InvalidClientIDException()
