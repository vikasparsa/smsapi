from django.test import TestCase
from requests.auth import HTTPBasicAuth
import requests
import json
import arrow

# Create your tests here.
class apiTests(TestCase):

    def setUp(self):
        self.headers = HTTPBasicAuth('azr2','54P2EOKQ47')

    def test_outbound_request_methods(self):
        response = requests.get('http://127.0.0.1:8000/outbound/sms/', auth=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_inbound_request_methods(self):
        response = requests.get('http://127.0.0.1:8000/inbound/sms/', auth=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_authentication(self):
        response = requests.post('http://127.0.0.1:8000/outbound/sms/', auth=HTTPBasicAuth('azr2','2EOKQ47'))
        self.assertEqual(response.status_code, 403)

    def test_from_validation(self):
        data = json.dumps({'to':'4924195509198','text':'Hello'})
        response_in = requests.post('http://127.0.0.1:8000/inbound/sms/', auth=self.headers, data=data)
        response_out = requests.post('http://127.0.0.1:8000/outbound/sms/', auth=self.headers, data=data)
        self.assertEqual(response_in.status_code, 200)
        self.assertEqual(response_out.status_code, 200)
        response_data_in = json.loads(response_in.content)
        response_data_out = json.loads(response_out.content)
        self.assertEqual(response_data_in['error'], "from is missing")
        self.assertEqual(response_data_out['error'], "from is missing")

        data = json.dumps({'to':'4924195509198','text':'Hello', 'from':443456})
        response_in = requests.post('http://127.0.0.1:8000/inbound/sms/', auth=self.headers, data=data)
        response_out = requests.post('http://127.0.0.1:8000/outbound/sms/', auth=self.headers, data=data)
        self.assertEqual(response_in.status_code, 200)
        self.assertEqual(response_out.status_code, 200)
        response_data_in = json.loads(response_in.content)
        response_data_out = json.loads(response_out.content)
        self.assertEqual(response_data_in['error'], "from is invalid")
        self.assertEqual(response_data_out['error'], "from is invalid")

        data = json.dumps({'from':'4924195509198','text':'Hello', 'to':'4924195509193'})
        response_in = requests.post('http://127.0.0.1:8000/outbound/sms/', auth=self.headers, data=data)
        self.assertEqual(response_in.status_code, 200)
        response_data_in = json.loads(response_in.content)
        self.assertEqual(response_data_in['error'], "from parameter not found")

    def test_to_validation(self):
        data = json.dumps({'from':'4924195509198','text':'Hello'})
        response_in = requests.post('http://127.0.0.1:8000/inbound/sms/', auth=self.headers, data=data)
        response_out = requests.post('http://127.0.0.1:8000/outbound/sms/', auth=self.headers, data=data)
        self.assertEqual(response_in.status_code, 200)
        self.assertEqual(response_out.status_code, 200)
        response_data_in = json.loads(response_in.content)
        response_data_out = json.loads(response_out.content)
        self.assertEqual(response_data_in['error'], "to is missing")
        self.assertEqual(response_data_out['error'], "to is missing")

        data = json.dumps({'from':'4924195509198','text':'Hello', 'to':443456})
        response_in = requests.post('http://127.0.0.1:8000/inbound/sms/', auth=self.headers, data=data)
        response_out = requests.post('http://127.0.0.1:8000/outbound/sms/', auth=self.headers, data=data)
        self.assertEqual(response_in.status_code, 200)
        self.assertEqual(response_out.status_code, 200)
        response_data_in = json.loads(response_in.content)
        response_data_out = json.loads(response_out.content)
        self.assertEqual(response_data_in['error'], "to is invalid")
        self.assertEqual(response_data_out['error'], "to is invalid")

        data = json.dumps({'from':'4924195509198','text':'Hello', 'to':'4924195509193'})
        response_in = requests.post('http://127.0.0.1:8000/inbound/sms/', auth=self.headers, data=data)
        self.assertEqual(response_in.status_code, 200)
        response_data_in = json.loads(response_in.content)
        self.assertEqual(response_data_in['error'], "to parameter not found")

    def test_text_validation(self):
        data = json.dumps({'from':'4924195509198','to':'4924195509193'})
        response_in = requests.post('http://127.0.0.1:8000/inbound/sms/', auth=self.headers, data=data)
        response_out = requests.post('http://127.0.0.1:8000/outbound/sms/', auth=self.headers, data=data)
        self.assertEqual(response_in.status_code, 200)
        self.assertEqual(response_out.status_code, 200)
        response_data_in = json.loads(response_in.content)
        response_data_out = json.loads(response_out.content)
        self.assertEqual(response_data_in['error'], "text is missing")
        self.assertEqual(response_data_out['error'], "text is missing")

        data = json.dumps({'to':'4924195509198','text':'', 'from':'4924195509193'})
        response_in = requests.post('http://127.0.0.1:8000/inbound/sms/', auth=self.headers, data=data)
        response_out = requests.post('http://127.0.0.1:8000/outbound/sms/', auth=self.headers, data=data)
        self.assertEqual(response_in.status_code, 200)
        self.assertEqual(response_out.status_code, 200)
        response_data_in = json.loads(response_in.content)
        response_data_out = json.loads(response_out.content)
        self.assertEqual(response_data_in['error'], "text is invalid")
        self.assertEqual(response_data_out['error'], "text is invalid")

    def test_stop_call(self):
        data = json.dumps({'from':'441224459590','to':'13602092244', 'text':'STOP'})
        response_in = requests.post('http://127.0.0.1:8000/inbound/sms/', auth=self.headers, data=data)
        self.assertEqual(response_in.status_code, 200)
        response_data_in = json.loads(response_in.content)
        self.assertEqual(response_data_in['message'], "inbound sms ok")

        data = json.dumps({'from':'441224459590','to':'13602092244', 'text':'Hello'})
        response_in = requests.post('http://127.0.0.1:8000/outbound/sms/', auth=self.headers, data=data)
        self.assertEqual(response_in.status_code, 200)
        response_data_in = json.loads(response_in.content)
        self.assertEqual(response_data_in['error'], "sms from 441224459590 to 13602092244 blocked by STOP request")

#Clear cache before running
    def test_requests_limit(self):
        data = json.dumps({'from':'441224980091','to':'13602092244', 'text':'Hellooo'})
        for i in range(52):
            response_in = requests.post('http://127.0.0.1:8000/outbound/sms/', auth=self.headers, data=data)
            self.assertEqual(response_in.status_code, 200)
            response_data_in = json.loads(response_in.content)
            if i>50:
                self.assertEqual(response_data_in['error'], "limit reached for from 441224980091")
            else:
                self.assertEqual(response_data_in['message'], "outbound sms ok")
