import requests
import json


def sendMessage(chat_object_id, message_content, api, host='127.0.0.1', port='5000', is_https=0):
    if is_https:
        communication_protocal_head = 'https://'
    else:
        communication_protocal_head = 'http://'
    url = communication_protocal_head + host + ':' + port + api
    payload = {'id': chat_object_id, 'content': message_content}
    resp = requests.get(url, params=payload)
    respDict = json.loads(resp.text)
    if not respDict['code']:
        return True
    else:
        return False


def sendFriendMessage(chat_object_id, message_content):
    resp = sendMessage(chat_object_id, message_content,
                       '/openqq/send_friend_message')
    return resp

def sendGroupMessage(chat_object_id, message_content):
    resp = sendMessage(chat_object_id, message_content,
                       '/openqq/send_group_message')
    return resp
