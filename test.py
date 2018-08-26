import handlePostData
import multiprocessing as mp
import time

def aaa(tmp_dict):
    while True:
        print("------")
        print(tmp_dict)
        time.sleep(1)

def job(q, path):
    messageDict = dict()
    while True:
        messageDict = handlePostData.getFriendsMessage(messageDict, path)
        print(messageDict)
        q.send(messageDict)

if __name__ == '__main__':
    manager = mp.Manager()
    receive_message_dict = manager.dict()
    #  receive_message_dict, p = mp.Pipe()
    tmp_dir = '/tmp/pyqtWebQQ/tmp/'
    #  p1 = mp.Process(target=job, args=(q,path))
    handle_friend_message = mp.Process(target=handlePostData.processGetFriendMessage,args= (receive_message_dict, tmp_dir, '/tmp/pyqtWebQQ/Message/'))
    handle_friend_message.start()
    while True:
        time.sleep(2)
        print("=====")
        print(receive_message_dict)

