from mirrserver.put_results_validator import PutResultsValidator
from mirrserver.put_results_validator import InvalidClientIDException
from mirrserver.put_results_validator import InvalidResultsException
import pytest


def test_put_results_with_non_numerical_client_id():
    validator = PutResultsValidator()
    data = {'results': {'': ''}, 'directory': None}
    client_id = 'a'
    with pytest.raises(InvalidClientIDException):
        validator.check_put_results(data, client_id)


def test_put_results_invalid_results():
    validator = PutResultsValidator()
    data = {'results': None, 'directory': None}
    client_id = '5'
    with pytest.raises(InvalidResultsException):
        validator.check_put_results(data, client_id)


def test_put_results_valid_client_id_and_results():
    validator = PutResultsValidator()
    data = {'results': {'': ''}, 'directory': None}
    client_id = '10'
    assert validator.check_put_results(data, client_id)
