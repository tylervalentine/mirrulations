import unittest
from unittest.mock import MagicMock, patch
from mirrcore.data_counts import DataCounts

class TestDataCounts(unittest.TestCase):

# Test that each count function returns the expected values
    @patch('requests.get')
    def test_get_counts(self, mock_api_request):
        """Tests that each count function returns the expected value"""
        # Set up mock data and objects
        api_key = "test"
        dockets_response = MagicMock()
        dockets_response.json.return_value = {"meta": {"totalElements": 500}}
        documents_response = MagicMock()
        documents_response.json.return_value = {"meta": {"totalElements": 1000}}
        comments_response = MagicMock()
        comments_response.json.return_value = {"meta": {"totalElements": 2500}}
        mock_api_request.side_effect = [dockets_response, documents_response, comments_response]


        # Call the function we want to test
        counts = DataCounts(api_key).get_counts()


        # Make assertions about the function's behavior
        self.assertEqual(counts, [500, 1000, 2500])  # Expected results

