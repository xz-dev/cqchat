import requests
import json

#resp = requests.get(url)
#resp_text = resp.text
# print(resp_text)
#resp_json = json.loads(resp_text)
#url = 'http://127.0.0.1:5000/openqq/check_event'
#resp = requests.get(url)


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
