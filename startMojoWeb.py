import subprocess
import time
import os
import shutil


def stopMojoWebQQ(tmp_dir):
    """
    阻塞型关闭客户端
    """
    args = ['killall', 'perl']
    proc = subprocess.Popen(args)
    # 新建缓存文件夹
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

def startMojoWebQQ(webqq_config_file_path):
    """
    启动客户端
    """
    os.remove('nohup.out') # 清除以前的nohup输出
    args = ['pidof', 'perl']
    proc = subprocess.Popen(args)
    while True:
        outs, errs = proc.communicate()
        if errs == None:
            break
        else:
            time.sleep(0.2)
    args = ['setsid', 'nohup', 'perl', webqq_config_file_path]
    proc = subprocess.Popen(args)


if __name__ == '__main__':
    startMojoWebQQ('webqq.pl')
