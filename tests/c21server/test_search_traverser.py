import json
from c21server.work_gen.search_traverser import SearchIterator
from c21server.work_gen.regulations_api import RegulationsAPI
from c21server.work_gen.mock_dataset import MockDataSet


def make_get_result(page_number, total_pages, total_results):

    if page_number == total_pages:
        num_results = 5
    else:
        num_results = 10
    data = [{'id': 'TEST-{}'.format(page_number * 10 + n)}
            for n in range(num_results)]

    meta = {
        'pageNumber': page_number,
        'pageSize': num_results,
        'totalElements': total_results,
        'totalPages': total_pages,
    }

    result = {'data': data,
              'meta': meta
              }

    return {'text': json.dumps(result)}


def test_iterate_one_page(requests_mock, mocker):
    mocker.patch('time.sleep')

    results = MockDataSet(150).get_results()

    requests_mock.get('https://api.regulations.gov/v4/documents', results)
    api = RegulationsAPI('FAKE_KEY')
    count = 0
    for _ in SearchIterator(api, 'documents', '2021-06-08 00:00:00'):
        count += 1

    assert count == 1


def test_iterate_four_pages(requests_mock, mocker):

    mocker.patch('time.sleep')

    results = MockDataSet(850).get_results()

    requests_mock.get('https://api.regulations.gov/v4/documents', results)
    api = RegulationsAPI('FAKE_KEY')
    count = 0
    for _ in SearchIterator(api, 'documents', '2021-06-08 00:00:00'):
        count += 1

    assert count == 4


def test_iterate_5650_results(requests_mock, mocker):

    mocker.patch('time.sleep')

    results = MockDataSet(5650).get_results()
    requests_mock.get('https://api.regulations.gov/v4/documents', results)
    api = RegulationsAPI('FAKE_KEY')

    count = 0
    for _ in SearchIterator(api, 'documents', '2021-06-08 00:00:00'):
        count += 1

    assert count == 23
