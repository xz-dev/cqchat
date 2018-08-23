import multiprocessing as mp
import threading
import datetime
import time

import startUi
import handlePostData
import startMojoWeb
from post import postServer

if __name__ == '__main__':
    try:
        mojo_webqq_config_path = 'webqq.pl'
        manager = mp.Manager()
        POST_data = manager.list()
        #  post_server, post_ui = mp.Pipe()
        receive_friend_message, def_receive_friend_message = mp.Pipe()
        # POST服务器
        post_server = mp.Process(
            target=postServer.run,
            args=(POST_data,))
        # mojo-webqq服务器
        webqq_server = mp.Process(
            target=startMojoWeb.startMojoWebQQ,
            args=(mojo_webqq_config_path,))
        # 确认启动mojo-webqq启动
        # 并显示二维码
        is_start = mp.Process(
            target=handlePostData.isStart,
            args=(POST_data,))
        # 显示主UI
        ui = mp.Process(target=startUi.main)
        handle_friend_message = mp.Process(
            target=handlePostData.processGetFriendMessage,
            args=(POST_data, def_receive_friend_message))
        startMojoWeb.stopMojoWebQQ()  # 完全关闭MojoWebQQ
        post_server.start()           # 启动POST服务器
        webqq_server.start()          # 启动MojoWebQQ
        # 等待mojo-webqq工作, 显示二维码
        is_start.start()
        is_start.join()
        # 扫码后启动主UI
        ui.start()
        #  handle_friend_message.start()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
