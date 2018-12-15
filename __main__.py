import multiprocessing as mp

from . import contact_ui as main_ui
from . import wechat, data

if __name__ == '__main__':
    try:
        mojo_webqq_config_path = 'webqq.pl'
        manager = mp.Manager()
        POST_data = manager.list()
        all_message_dict = manager.dict()
        PostServer = wechat.post.server.PostServer()
        Data = data.Data()
        HandlePostData = wechat.data.data_handle.HandlePostData()
        post_server = mp.Process(
            target=PostServer.run, args=(Data.post_data, ))
        post_handle = mp.Process(target=HandlePostData.run, args=(Data, ))
        post_handle.start()
        post_server.start()
        main_ui.main(Data)
        post_handle.join()
        post_server.join()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
