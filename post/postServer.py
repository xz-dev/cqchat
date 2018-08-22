#!/usr/bin/env python3
"""
Very simple HTTP server in python
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import datetime

global tmp_dir


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        # Gets the size of data
        post_data = self.rfile.read(content_length)
        # Gets the data itself
        resp_json = json.loads(post_data.decode('utf-8'))  # 获取POST json
        #  print(resp_json)
        writeJson(resp_json, tmp_dir)  # 写入POST数据
        self._set_response()
        self.wfile.write("POST request for {}".format(
            self.path).encode('utf-8'))


def writeJson(resp_json, tmp_dir):
    mkdir(tmp_dir)  # 创建缓存文件夹
    tmp_file = tmp_dir + '/' + str(datetime.datetime.utcnow())
    with open(tmp_file, 'w') as f:
        json.dump(resp_json, f)


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def rmdir(path):
    file_list = os.listdir(path)
    if not len(file_list):
        os.rmdir(path)


def run(temp_dir, server_class=HTTPServer, port=5001):
    global tmp_dir
    tmp_dir = temp_dir
    handler_class = S
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        #  rmdir(tmp_dir)
        pass
    httpd.server_close()


if __name__ == '__main__':
    run('/tmp/pyqtWebQQ/tmp/')
