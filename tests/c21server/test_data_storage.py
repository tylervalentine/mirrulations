
import pytest
from c21server.core.config import settings
from c21server.work_gen.data_storage import DataStorage


# docs have 'scope="session", autouse=True' as parameters,
# but pylint complains.  This version works, but it requires
# that you add 'set_test_settings' as a parameter to each
# test.  Note, pylint_pytest is used to ignore the unused
# variable on test functions
@pytest.fixture()
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")


def exists(storage, the_id):
    assert storage.exists({'id': the_id})


def does_not_exist(storage, the_id):
    assert storage.exists({'id': the_id}) is False


def test_data_knows_about_existing_files(set_test_settings):
    storage = DataStorage()

    # docket exists
    exists(storage, 'OCC-2020-0031')

    # docket does not exist
    does_not_exist(storage, 'OCC-2020-9999')

    # document exists
    exists(storage, 'OCC-2020-0031-0001')

    # document does not exist
    does_not_exist(storage, 'OCC-2020-0031-9999')

    # comment exists
    exists(storage, 'OCC-2020-0031-0008')

    # comment does not exist
    does_not_exist(storage, 'OCC-2020-0031-9999')
