import requests
import json

__all__ = [
    'post_data',
]


def post_data(payload, api='', is_https=0, host='127.0.0.1', port='8000'):
    transfer_protocol = 'http'
    if is_https:
        transfer_protocol = 'https'
    url = transfer_protocol + '://' + host + ':' + port + api
    resp = requests.post(url, data=json.dumps(payload))
    return resp
