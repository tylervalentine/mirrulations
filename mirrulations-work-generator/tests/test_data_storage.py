
from mirrgen.data_storage import DataStorage


def exists(storage, the_id):
    assert storage.exists({'id': the_id})


def does_not_exist(storage, the_id):
    assert storage.exists({'id': the_id}) is False


class FindOnly:
    def __init__(self, value):
        self.value = value

    def count_documents(self, search):
        if search['id'] == self.value:
            return 1
        return 0


def test_docket_found_others_not(monkeypatch):
    storage = DataStorage()

    monkeypatch.setattr(storage, 'dockets', FindOnly('DOCK-2020-1234'))
    monkeypatch.setattr(storage, 'documents', FindOnly('NOTHING'))
    monkeypatch.setattr(storage, 'comments', FindOnly('NOTHING'))

    # docket exists
    exists(storage, 'DOCK-2020-1234')
    # document does not exist
    does_not_exist(storage, 'DOC-2020-1234')
    # comment does not exist
    does_not_exist(storage, 'COM-2020-1234')


def test_document_found_others_not(monkeypatch):
    storage = DataStorage()

    monkeypatch.setattr(storage, 'dockets', FindOnly('NOTHING'))
    monkeypatch.setattr(storage, 'documents', FindOnly('DOC-2020-1234'))
    monkeypatch.setattr(storage, 'comments', FindOnly('NOTHING'))

    # docket does not exists
    does_not_exist(storage, 'DOCK-2020-1234')
    # document does exist
    exists(storage, 'DOC-2020-1234')
    # comment does not exist
    does_not_exist(storage, 'COM-2020-1234')


def test_comment_found_others_not(monkeypatch):
    storage = DataStorage()

    monkeypatch.setattr(storage, 'dockets', FindOnly('NOTHING'))
    monkeypatch.setattr(storage, 'documents', FindOnly('NOTHING'))
    monkeypatch.setattr(storage, 'comments', FindOnly('COM-2020-1234'))

    # docket does not exist
    does_not_exist(storage, 'DOCK-2020-1234')

    # document does not exist
    does_not_exist(storage, 'DOC-2020-1234')

    # comment exists
    exists(storage, 'COM-2020-1234')
