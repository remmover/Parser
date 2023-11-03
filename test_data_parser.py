import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

import requests

from data_parser import parse_webpage, parse_file, parse_database


class TestDataParserFunctions(unittest.TestCase):

    @patch('requests.get')
    def test_parse_webpage(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<html><h1>Test H1</h1></html>"
        result = parse_webpage('https://example.com')
        self.assertIsInstance(result, dict)
        self.assertIn('h1', result)
        self.assertEqual(result['h1'][0], 'Test H1')

        mock_get.side_effect = requests.RequestException("Request error")
        result = parse_webpage('https://nonexistent-website.com')
        self.assertIsInstance(result, str)
        self.assertIn('Request error occurred', result)

    def test_parse_file(self):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
            temp_file.write(b"name,value\nItem 1,10\nItem 2,20")
            temp_file_path = temp_file.name

        result = parse_file(temp_file_path, 'csv')
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(item, dict) for item in result))

        os.remove(temp_file_path)

    @patch('sqlite3.connect')
    @patch('pandas.read_sql_query')
    def test_parse_database(self, mock_read_sql_query, mock_connect):
        mock_connect.return_value.__enter__.return_value = mock_connect
        mock_read_sql_query.return_value.to_dict.return_value = [{'name': 'Item 1', 'value': 10}]
        result = parse_database('example.db', 'SELECT * FROM table_name')
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(item, dict) for item in result))

        mock_connect.side_effect = sqlite3.Error("Database error")
        result = parse_database('nonexistent.db', 'SELECT * FROM table_name')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
