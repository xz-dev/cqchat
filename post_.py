import requests
import json
#import os

#os.system('perl webqq.pl')
url = 'http://127.0.0.1:5000/openqq/get_client_info'
resp = requests.get(url)
resp_text = resp.text
print(resp_text)
resp_json = json.loads(resp_text)
#url = 'http://127.0.0.1:5000/openqq/check_event'
#resp = requests.get(url)

#payload = {'name': 'ZERO', 'content': 'test'}
#url = 'http://127.0.0.1:5000/openqq/send_friend_message'
#resp = requests.get(url, params=payload)
# print(resp.url)
# print(resp.text)
