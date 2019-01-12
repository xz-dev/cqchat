import requests
import json

__all__ = [
    'get_data',
]


def get_data(payload, api, is_https=0, host='127.0.0.1', port='5700'):
    transfer_protocol = None
    if is_https:
        transfer_protocol = 'https'
    else:
        transfer_protocol = 'http'
    url = transfer_protocol + '://' + host + ':' + port + api
    try:
        resp = requests.get(url, params=payload)
        resp.encoding = 'utf-8'  # 限定为utf-8编码, 避免乱码
        resp_data = json.loads(resp.text)
        return resp_data
    except Exception:
        return None
