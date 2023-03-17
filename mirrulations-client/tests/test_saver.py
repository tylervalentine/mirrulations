from mirrclient.saver import Saver
from unittest.mock import patch, mock_open
from json import dumps

def test_save_path_directory_does_not_already_exist():
    with patch('os.makedirs') as mock_dir:
        saver = Saver()
        saver.make_path('/USTR')
        mock_dir.assert_called_once_with('/data/USTR')


def test_save_path_directory_already_exists(capsys):
    with patch('os.makedirs') as mock_dir:
        saver = Saver()
        mock_dir.side_effect = FileExistsError('Directory already exists')
        saver.make_path('/USTR')

        print_data = 'Directory already exists in root: /data/USTR\n'
        captured = capsys.readouterr()
        assert captured.out == print_data

def test_save_json():
    saver = Saver()
    path = 'data/USTR/file.json'
    data = { 'results': 'Hello world' }

    with patch('mirrclient.saver.open', mock_open()) as mocked_file:
            saver.save_json(path, data)
            mocked_file.assert_called_once_with(path, 'w+', encoding='utf8')
            mocked_file().write.assert_called_once_with(dumps(data['results']))

def test_save_attachment():
    saver = Saver()
    path = 'data/USTR/file.pdf'
    data = 'Some Binary'

    with patch('mirrclient.saver.open', mock_open()) as mocked_file:
            saver.save_attachment(path, data)
            mocked_file.assert_called_once_with(path, 'wb')
            mocked_file().write.assert_called_once_with(data)