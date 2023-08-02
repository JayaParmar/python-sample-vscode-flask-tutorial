import unittest
from app import app, before_request, flask_logger, setup_logger
import uuid

class TestEndpoints(unittest.TestCase):

    def setUp(self):
        # SetUp prepares the test fixture
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        
    def tearDown(self):
        # Tear down after the results are recorded
        self.ctx.pop()

    def emit(self, record):
        self.log_buffer.append(record.getMessage())

    # Testing endpoint @app.route('/')
    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Welcome to the Orion Customer Dashboard API')

    # Testing endpoint @app.route('/customer', methods=['GET'])
    def test_customer_id_device_id_only_route(self):
        response = self.client.get('/customer?customer-id=1010')
        self.assertEqual(response.status_code, 200)

    # Testing endpoint @app.errorhandler(Exception)
    def test_handle_error_route(self):
        with self.assertRaises(Exception):
            self.app.get('/invalid-endpoint')

if __name__ == '__main__':
    unittest.main()
