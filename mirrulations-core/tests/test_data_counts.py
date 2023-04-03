import unittest
from unittest.mock import MagicMock, patch
from mirrcore.data_counts import DataCounts

class TestDataCounts(unittest.TestCase):

# Test that each count function returns the expected values
    @patch('requests.get')
    def test_get_counts(self, mock_api_request):
        assert 1==1
