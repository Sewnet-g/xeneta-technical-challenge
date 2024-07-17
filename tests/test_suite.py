import unittest
from unittest.mock import patch, MagicMock

from app import create_app


class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @patch('app.routes.get_db_connection')
    def test_get_rates(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = [
            {'day': '2016-01-01', 'average_price': 100},
            {'day': '2016-01-02', 'average_price': 150},
            {'day': '2016-01-03', 'average_price': 200}
        ]
        mock_get_db_connection.return_value = mock_conn

        response = self.client.get(
            '/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertTrue(all('day' in item and 'average_price' in item for item in data))

    def test_missing_parameters(self):
        response = self.client.get('/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_invalid_date_format(self):
        response = self.client.get(
            '/rates?date_from=invalid_date&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid date format. Please use YYYY-MM-DD format.')

    @patch('app.routes.get_db_connection')
    def test_empty_results(self, mock_get_db_connection):
        # Mock the database connection and cursor for empty results
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = []
        mock_get_db_connection.return_value = mock_conn

        response = self.client.get(
            '/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    @patch('app.routes.get_db_connection')
    def test_internal_server_error(self, mock_get_db_connection):
        # Mock the database connection to raise an exception
        mock_get_db_connection.side_effect = Exception("Database connection error")

        response = self.client.get(
            '/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main')
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'An unexpected error occurred. Please try again later.')


if __name__ == '__main__':
    unittest.main()
