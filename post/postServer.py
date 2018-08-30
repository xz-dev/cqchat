#!/usr/bin/env python3
"""
HTTP 服务器部分的实现参考
https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7
Thanks mdonkers!
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time

global post_data_list


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        # Gets the size of data
        content_length = int(self.headers['Content-Length'])
        # Gets the data itself
        post_data = self.rfile.read(content_length)
        # 获取POST json并写入post_data_list
        post_json = json.loads(post_data.decode('utf-8'))
        post_json['local_unix_time'] = time.time()
        #  print(post_json)
        post_data_list.append(post_json)
        self._set_response()
        self.wfile.write("POST request for {}".format(
            self.path).encode('utf-8'))


def run(POST_data, server_class=HTTPServer, port=5001):
    global post_data_list
    post_data_list = POST_data
    handler_class = S
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        while POST_data != False:
            httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


#  if __name__ == '__main__':
#      run('/tmp/pyqtWebQQ/tmp/')
