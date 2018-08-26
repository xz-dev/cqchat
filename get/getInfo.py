import requests
import json


def getInfo(is_https, host, port, api):
    if is_https:
        transfer_protocol = 'https'
    else:
        transferProtocol = 'http'
    url = transferProtocol + '://' + host + ':' + port + api
    resp = requests.get(url)
    resp.encoding = 'utf-8'  # 限定为utf-8编码, 避免乱码
    info_list = json.loads(resp.text)
    return info_list


def getGroupInfo(is_https=0, host='127.0.0.1', port='5000', api='/openqq/get_group_info'):
    group_info_list = getInfo(
        is_https=is_https, host=host, port=port, api=api)
    return group_info_list


def getFriendInfo(is_https=0, host='127.0.0.1', port='5000', api='/openqq/get_friend_info'):
    friend_info_list = getInfo(
        is_https=is_https, host=host, port=port, api=api)
    return friend_info_list
