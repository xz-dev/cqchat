import multiprocessing as mp

from .ui.code import Ui
from .server.post.PostServer import PostServer
from .server.data import data_api, data

if __name__ == '__main__':
    try:
        Data = data.Data()
        HandlePostData = data_api.auto_handle.HandlePostData(Data)
        AutoFlashData = data_api.auto_flash_data.AutoFlashData(Data)
        PostServer = PostServer(Data.post_data)
        # POST服务器
        print(Data.ui_data.chat_object)
        post_server = mp.Process(target=PostServer.run)
        post_handle = mp.Process(target=HandlePostData.run)
        # 显示主UI
        ui = mp.Process(target=Ui.main, args=(Data, ))
        ui.start()
        post_handle.start()
        post_server.start()
        ui.join()
        post_server.join()
        post_handle.join()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
