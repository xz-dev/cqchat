import requests
import json


def getFriendInfo(isHttps=0, host='127.0.0.1', port='5000', api='/openqq/get_friend_info'):
    if isHttps:
        transferProtocol = 'https'
    else:
        transferProtocol = 'http'
    url = transferProtocol + '://' + host + ':' + port + api
    resp = requests.get(url)
    respDict = json.loads(resp.text)
    return respDict


def getName(respDict):
    """
    获取friendInfo中的昵称与ID信息
    """
    infoDict = dict()
    categoryList = list()
    allNumber = len(respDict)
    for n in range(allNumber):
        tempId = respDict[n]['id']
        name = respDict[n]['name']
        category = respDict[n]['category']
        if category not in categoryList:
            categoryList.append(category)
        infoDict[tempId] = {'name': name,
                            'category': category}
    return infoDict, categoryList
