import requests as req


class BEXiAdapter:

    MSG_HTTP_ERR = "Il server ha restituito un errore. {}"
    MSG_TIMEOUT_ERR = "La richiesta è andata in timeout. {}"
    MSG_REDIRECT_ERR = "Il server ha effettuato troppi redirect. {}"
    MSG_GENERIC_ERR = "Qualcosa è andato storto nell'invio della richiesta. {}"
    TIMEOUT_SETTINGS = (5, 20)
    
    def __init__(self, endpoint):
        self._token_url = endpoint.token_url
        self._adapter_url = endpoint.adapter_url
        self._credentials = endpoint.credentials

    def get_token(self):
        try:
            response = req.get(self._token_url,
                               data=self._credentials,
                               timeout=BEXiAdapter.TIMEOUT_SETTINGS)
            response.raise_for_status()
            return response.json()
        except req.exceptions.HTTPError as httpex:
            raise Exception(BEXiAdapter.MSG_HTTP_ERR.format(str(httpex)))
        except req.exceptions.Timeout as timeoutex:
            raise Exception(BEXiAdapter.MSG_TIMEOUT_ERR.format(str(timeoutex)))
        except req.exceptions.TooManyRedirects as redirex:
            raise Exception(BEXiAdapter.MSG_REDIRECT_ERR.format(str(redirex)))
        except req.exceptions.RequestsException as reqex:
            raise Exception(BEXiAdapter.MSG_GENERIC_ERR.format(str(reqex)))
        except Exception as e:
            raise Exception(BEXiAdapter.MSG_GENERIC_ERR.format(str(e)))

    def start_new_task(self, json_token, json_body):
        try:        
            headers = self._get_request_headers(json_token)
            response = req.post(self._adapter_url,
                                data=json_body,
                                headers=headers,
                                timeout=BEXiAdapter.TIMEOUT_SETTINGS)
            response.raise_for_status()
            return response.json()
        except req.exceptions.HTTPError as httpex:
            raise Exception(BEXiAdapter.MSG_HTTP_ERR.format(str(httpex)))
        except req.exceptions.Timeout as timeoutex:
            raise Exception(BEXiAdapter.MSG_TIMEOUT_ERR.format(str(timeoutex)))
        except req.exceptions.TooManyRedirect as redirex:
            raise Exception(BEXiAdapter.MSG_REDIRECT_ERR.format(str(redirex)))
        except req.exceptions.RequestException as reqex:
            raise Exception(BEXiAdapter.MSG_GENERIC_ERR.format(str(reqex)))
        except Exception as e:
            raise Exception(BEXiAdapter.MSG_GENERIC_ERR.format(str(e)))

    def _get_request_headers(self, json_token):
        access_token = json_token['access_token']
        headers = {'Content-Type':'application/json',
                 'Authorization':'Bearer {}'.format(access_token),
                 'cache-control':'no-cache'}
        return headers


