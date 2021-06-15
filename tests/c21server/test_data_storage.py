import json
from c21server.work_gen.data_storage import DataStorage


def load_data(filename):
    filepath = f'tests/data/{filename}'
    return json.loads(open(filepath).read())


def test_data_knows_about_existing_files():
    storage = DataStorage()

    assert storage.exists(load_data('comment_found.json')) is True

    # Search for comment when docket not present
    assert storage.exists(load_data('comment_not_found.json')) is False

    # Search for comment when other comments present
    assert storage.exists({'id': 'OCC-2020-0031-9999'}) is False

    # search for docket
    assert storage.exists({'id': 'NIH-2006-1094'}) is True

    # This docket has 750K comments.  Search for one that is not present
    # This works, but it takes 5 minutes
    # assert storage.exists({'id': 'CEQ-2019-0003-999999'}) is False
    # And this one still takes 30+ seconds, but works...
    # assert storage.exists({'id': 'CEQ-2019-0003-99999'})
