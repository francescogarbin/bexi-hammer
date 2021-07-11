import json
import requests as req

class BEXiAdapter:

    def __init__(self, token_url, adapter_url):
        self._token_url = token_url
        self._adapter_url = adapter_url
        self._token = None


    def post_request(self, json_credentials, json_payload):
        if self._get_token(json_credentials):
            return self._post_start_new_task(json_payload)
        return None


    def _get_request_headers(self):
        token = self._token['access_token']
        headers = {'Content-Type':'application/json',
                 'Authorization':'Bearer {}'.format(token),
                 'cache-control':'no-cache'}
        return headers

    def _get_token(self, json_credentials):
        response = req.get(self._token_url,
                           data=json_credentials,
                           timeout=(5, 20))
        if response.status_code == 200:
            self._token = response.json()
            return self._token
        print("TOKEN NON RECUPERATO")
        return None


    def _post_start_new_task(self, json_payload):
        headers = self._get_request_headers()
        response = req.post(self._adapter_url,
                            data=json_payload,
                            headers=headers,
                            timeout=(5, 20))
        if response.status_code == 200:
            return response.json()
        print("RESPONSE NON RECUPERATA")
        return None



