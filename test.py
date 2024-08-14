import unittest
import json
from unittest.mock import patch, mock_open
from stark.invoice import app

class TestWebHook(unittest.TestCase):
    def setUp(self):
        """Set up the test client."""
        self.client = app.test_client()
        self.client.testing = True

    def test_start_invoices(self):
        """Test the /start-invoices endpoint."""
        response = self.client.post('/start-invoices')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Invoice creation started'})

    @patch('stark.invoice.open', new_callable=mock_open, read_data=json.dumps({
        'tax_id': '12345678901',
        'name': 'Test Bank',
        'bank_code': '001',
        'branch_code': '1234',
        'account_number': '00012345',
        'account_type': 'checking'
    }))
    @patch('stark.invoice.starkbank.transfer.create')
    def test_create_transfers(self, mock_transfer_create, mock_open):
        """Test the /create-transfer endpoint."""
        mock_transfer_create.return_value = [{'id': 'transfer_id'}]
        json_data = {
            "event": {
                "subscription": "invoice",
                "log": {
                    "invoice": {
                        "amount": 10000,
                        "fee": 500
                    }
                }
            }
        }
        response = self.client.post('/create-transfer', json=json_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success'})

    @patch('stark.invoice.open', new_callable=mock_open, read_data=json.dumps({}))
    def test_create_transfers_error(self, mock_open):
        """Test the /create-transfer endpoint with error."""
        json_data = {
            "event": {
                "subscription": "invoice",
                "log": {}
            }
        }
        
        # Send POST request to the /create-transfer endpoint
        response = self.client.post('/create-transfer', json=json_data)
        
        self.assertEqual(response.status_code, 400)
        
        self.assertEqual(response.json, {'status': 'error', 'message': 'No Amount'})
        
        mock_open.assert_not_called()

if __name__ == '__main__':
    unittest.main()
