import multiprocessing as mp

#  from . import mojo
from . import main_ui
from .post.PostServer import PostServer
from .data import data_handle, data

if __name__ == '__main__':
    try:
        mojo_webqq_config_path = 'webqq.pl'
        manager = mp.Manager()
        POST_data = manager.list()
        all_message_dict = manager.dict()
        PostServer = PostServer()
        Data = data.Data()
        HandlePostData = data_handle.HandlePostData()
        # mojo-webqq服务器
        #  webqq_server = mp.Process(
        #      target=mojo.startMojoWebQQ, args=(mojo_webqq_config_path, ))
        # POST服务器
        post_server = mp.Process(
            target=PostServer.run, args=(Data.post_data, ))
        post_handle = mp.Process(target=HandlePostData.run, args=(Data, ))
        # 显示主UI
        #  Ui = mp.Process(
        #      target=Ui.main, args=(Data, ))
        #  Ui.start()
        post_handle.start()
        post_server.start()
        #  webqq_server.start()
        main_ui.main(Data)
        #  Ui.join()
        post_handle.join()
        post_server.join()
        #  # POST信息处理
        #  handle_friend_message = mp.Process(
        #      target=handlePostData.getMessage,
        #      args=(POST_data, all_message_dict))
        #  # 显示主UI
        #  ui = mp.Process(
        #      target=Ui.main, args=(all_message_dict, POST_data, ))
        #  startMojoWeb.stopMojoWebQQ()  # 完全关闭MojoWebQQ
        #  post_server.start()           # 启动POST服务器
        #  # 扫码后启动好友消息处理程序
        #  #  handle_friend_message.start()
        #  # 启动主页UI
        #  ui.start()
        #  ui.join()
        #  # UI关闭, POST_data = False 以示程序关闭
        #  POST_data = False
        #  handle_friend_message.join()
        #  webqq_server.join()
        #  post_server.join()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
