import subprocess
import time
import os
import shutil


def stopMojoWebQQ():
    """
    阻塞型关闭客户端
    """
    args = ['killall', 'perl']
    proc = subprocess.Popen(args)

def startMojoWebQQ(mojo_webqq_config_path):
    """
    启动客户端
    """
    if os.path.exists('nohup.out'):
        os.remove('nohup.out') # 清除以前的nohup输出
    args = ['setsid', 'nohup', 'perl', mojo_webqq_config_path]
    proc = subprocess.Popen(args)

if __name__ == '__main__':
    startMojoWebQQ('webqq.pl')
