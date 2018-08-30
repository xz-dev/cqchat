import multiprocessing as mp

import Ui
import handlePostData
import startMojoWeb
from post import postServer

if __name__ == '__main__':
    try:
        mojo_webqq_config_path = 'webqq.pl'
        manager = mp.Manager()
        POST_data = manager.list()
        all_message_dict = manager.dict()
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
        # 消息处理
        handle_friend_message = mp.Process(
            target=handlePostData.getMessage,
            args=(POST_data, all_message_dict))
        # 显示主UI
        ui = mp.Process(
            target=Ui.main, args=(all_message_dict,))
        startMojoWeb.stopMojoWebQQ()  # 完全关闭MojoWebQQ
        post_server.start()           # 启动POST服务器
        webqq_server.start()          # 启动MojoWebQQ
        # 等待mojo-webqq工作, 显示二维码
        is_start.start()
        is_start.join()
        # 扫码后启动好友消息处理程序
        handle_friend_message.start()
        # 启动主页UI
        ui.start()
        ui.join()
        # UI关闭, POST_data = False 以示程序关闭
        POST_data = False
        handle_friend_message.join()
        webqq_server.join()
        post_server.join()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
