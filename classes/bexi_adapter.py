import json
import requests as req

class BEXiAdapter:

    def __init__(self, token_url, adapter_url):
        self._token_url = token_url
        self._adapter_url = adapter_url
        

    def get_token(self, json_credentials):
        response = req.get(self._token_url,
                           data=json_credentials,
                           timeout=(5, 20))
        return response


    def post_start_new_task(self, json_token, json_body):
        headers = self._get_request_headers(json_token)
        response = req.post(self._adapter_url,
                            data=json_body,
                            headers=headers,
                            timeout=(5, 20))
        return response


    def _get_request_headers(self, json_token):
        access_token = json_token['access_token']
        headers = {'Content-Type':'application/json',
                 'Authorization':'Bearer {}'.format(access_token),
                 'cache-control':'no-cache'}
        return headers


