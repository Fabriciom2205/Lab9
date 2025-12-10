import unittest
import json
from my_server import app, token_storage

class TestTokenService(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        token_storage.clear()
    
    def test_1_create_token(self):
        response = self.app.post('/create-token',
                                 json={'id': 'test@uconn.edu'},
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        print("Token created successfully")
    
    def test_2_verify_valid_token(self):
        create_resp = self.app.post('/create-token',
                                   json={'id': 'student@uconn.edu'},
                                   content_type='application/json')
        token = json.loads(create_resp.data)['uuid-token']
        
        verify_resp = self.app.post('/verify-token',
                                   json={'uuid-token': token},
                                   content_type='application/json')
        
        self.assertEqual(verify_resp.status_code, 200)
        print("Valid token verified")
    
    def test_3_reject_fake_token(self):
        response = self.app.post('/verify-token',
                                json={'uuid-token': 'fake-token'},
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
        print("Fake token rejected")

if __name__ == '__main__':
    unittest.main(verbosity=2)