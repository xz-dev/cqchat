def readlines(log_file):
    """
    读取mojo log文件
    """
    mojo_log_list = list()
    try:
        with open(log_file, 'r') as f:
            mojo_log_list = f.readlines()
        open(log_file,'w').close()
    finally:
        return mojo_log_list
