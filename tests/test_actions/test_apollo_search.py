import json
from unittest import TestCase, mock

from lagent.actions import GoogleSearch
from lagent.schema import ActionStatusCode, ActionReturn


class TestGoogleSearch(TestCase):

    @mock.patch.object(GoogleSearch, '_search')
    def test_search_tool(self, mock_search_func):
        # Load mock data from file
        with open('tests/data/search.json', 'r') as f:
            mock_data = json.load(f)
        mock_response = (200, mock_data)
        mock_search_func.return_value = mock_response
        
        search_tool = GoogleSearch(api_key='abc')
        tool_return = search_tool.run("What's the capital of China?")
        
        self.assertEqual(tool_return.status, ActionStatusCode.SUCCESS)
        self.assertEqual(tool_return.result, "Beijing")

    @mock.patch.object(GoogleSearch, '_search')
    def test_api_error(self, mock_search_func):
        mock_response = (403, {'message': 'bad requests'})
        mock_search_func.return_value = mock_response
        
        search_tool = GoogleSearch(api_key='abc')
        tool_return = search_tool.run("What's the capital of China?")
        
        self.assertEqual(tool_return.status, ActionStatusCode.API_ERROR)
        self.assertEqual(tool_return.errmsg, "API Error: 403 - bad requests")

    @mock.patch.object(GoogleSearch, '_search')
    def test_http_error(self, mock_search_func):
        mock_response = (-1, 'HTTPSConnectionPool')
        mock_search_func.return_value = mock_response
        
        search_tool = GoogleSearch(api_key='abc')
        tool_return = search_tool.run("What's the capital of China?")
        
        self.assertEqual(tool_return.status, ActionStatusCode.HTTP_ERROR)
        self.assertEqual(tool_return.errmsg, "HTTP Error: HTTPSConnectionPool")

    @mock.patch.object(GoogleSearch, '_search')
    def test_apollo_api_key(self, mock_search_func):
        # Mock API response
        mock_response = (200, {'items': [{'snippet': 'Test result'}]})
        mock_search_func.return_value = mock_response

        # Create GoogleSearch instance with Apollo API key
        apollo_api_key = "XA_qBepkTI5yPqZrelYqTw"
        search_tool = GoogleSearch(api_key=apollo_api_key)

        # Run a search query
        tool_return = search_tool.run("Test query")

        # Assert that the search was successful
        self.assertEqual(tool_return.status, ActionStatusCode.SUCCESS)
        self.assertEqual(tool_return.result, "Test result")

        # Assert that the API key was used in the search request
        mock_search_func.assert_called_once()
        call_args = mock_search_func.call_args[0][0]
        self.assertIn(apollo_api_key, call_args)
