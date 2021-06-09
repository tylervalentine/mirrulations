import pytest
from c21server.work_gen.regulations_api import RegulationsAPI, MIN_DELAY_BETWEEN_CALLS
from requests import HTTPError


def test_download_returns_json(requests_mock):
    requests_mock.get(
        'http://a.b.c',
        json={'foo': 'bar'}
    )
    api = RegulationsAPI('FAKE_KEY')

    result = api.download('http://a.b.c')
    expected = {'foo': 'bar'}
    assert result == expected


def test_404_raises_exception(requests_mock):
    requests_mock.get(
        'http://a.b.c',
        status_code=404
    )
    api = RegulationsAPI('FAKE_KEY')

    with pytest.raises(HTTPError):
        api.download('http://a.b.c')


def test_sleep_called_when_multiple_downloads(requests_mock, mocker):
    requests_mock.get(
        'http://a.b.c',
        json={'foo': 'bar'}
    )
    api = RegulationsAPI('FAKE_KEY')

    fake_time = mocker.patch('time.sleep')

    api.download('http://a.b.c')
    # assert no sleep
    assert not fake_time.called
    api.download('http://a.b.c')
    assert fake_time.called
    fake_time.assert_called_with(MIN_DELAY_BETWEEN_CALLS)


def test_params_passed(requests_mock):
    requests_mock.get(
        'http://a.b.c', json={'foo': 'bar'}
    )

    params = {'key': 'value'}

    api = RegulationsAPI('FAKE_KEY')
    api.download('http://a.b.c', params=params)

    call = requests_mock.request_history[0]
    # URL should be http://a.b.c?=key=value&api_key=FAKE_KEY
    # Since the order of the params could be changed, I just look
    # for the string in the overall url
    assert 'key=value' in call.url

