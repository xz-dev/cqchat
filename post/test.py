import multiprocessing as mp
import time

import postServer
if __name__ == '__main__':
    manager = mp.Manager()
    POST_data = manager.list()
    post_server = mp.Process(target=postServer.run, args=(POST_data,))
    post_server.start()
    while True:
        print(POST_data)
        time.sleep(2)
