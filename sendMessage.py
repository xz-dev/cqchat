import requests
import json


def sendFriendMessage(tempId, content):
    payload = {'id': tempId, 'content': content}
    url = 'http://127.0.0.1:5000/openqq/send_friend_message'
    resp = requests.get(url, params=payload)
    respDict = json.loads(resp.text)
    if not respDict['code']:
        return True
    else:
        return False


def isSuccess(resp):
    if resp['code'] == 0:
        return True
    else:
        return False
