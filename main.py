import multiprocessing as mp
import threading
import datetime
import time

import startUi
import handlePostData
import startMojoWeb
from post import postServer

# TODO: 在没有缓存文件夹的情况下,需要手动创建缓存文件夹,否则,程序json处理部分报错
# 报错代码: json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
# 报错部分: handlePostData.py 第69行
if __name__ == '__main__':
    try:
        #  lock_file = '/tmp/isStartWebQQ.lock'
        #  post_server, post_ui = mp.Pipe()
        tmp_dir_path = '/tmp/pyqtWebQQ/tmp/'
        bak_friend_message_path = '/tmp/pyqtWebQQ/Message/Friend/'
        receive_friend_message, def_receive_friend_message = mp.Pipe()
        post_server = mp.Process(
            target=postServer.run, args=(tmp_dir_path,))
        start_time = datetime.datetime.utcnow()
        webqq_server = mp.Process(
            target=startMojoWeb.startMojoWebQQ, args=('webqq.pl',))
        is_start = mp.Process(target=handlePostData.isStart,
                              args=(tmp_dir_path, start_time,))
        ui = mp.Process(target=startUi.main)
        handle_friend_message = mp.Process(target=handlePostData.processGetFriendMessage, args=(
            def_receive_friend_message, tmp_dir_path, bak_friend_message_path))
        startMojoWeb.stopMojoWebQQ(tmp_dir_path)  # 完全关闭MojoWebQQ
        time.sleep(0.5)
        # 避免因perl未停止导致的报错
        # TODO: https://github.com/sjdy521/Mojo-Webqq/blob/master/API.md#%E7%BB%88%E6%AD%A2%E7%A8%8B%E5%BA%8F%E8%BF%90%E8%A1%8C
        post_server.start()
        webqq_server.start()  # 启动MojoWebQQ
        #  server.join()
        is_start.start()
        is_start.join()
        # 等待扫码
        ui.start()
        #  handle_friend_message.start()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
