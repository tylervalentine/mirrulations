from mirrserver.exceptions import InvalidClientIDException


class GetClientIDValidator():
    """Validates the client_id sent by the client"""
    def check_get_client_id(self, client_id):
        if client_id is None:
            client_id = '1'
            return True
        if client_id.isdigit() or isinstance(client_id, int):
            client_id = int(client_id)
            if 0 < client_id < 20:
                return True
        raise InvalidClientIDException()
