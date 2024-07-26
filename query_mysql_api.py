import pandas as pd
import pymysql


from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = self.get_path()
        if path == '/test':
            params = self.get_params()
            # http://localhost:8000/test?a=1&b=2
            # print(params['a'][0], '---------')
            # print(params['b'][0], '---------')
            print(params, '---------')
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            resp = self.test()
            self.wfile.write(json.dumps(resp).encode('utf-8'))

    def get_path(self):
        return self.path.split('?')[0]

    def get_params(self):
        if len(self.path.split('?')) > 1:
            # 解析查询字符串
            params = parse_qs(self.path.split('?')[1])  
        else:
            params = {}
        return params

    def get_connection(self):
        # 设置数据库连接参数
        db_connection = pymysql.connect(host='192.168.0.122',
                                    user='root',
                                    password='hxkj2023',
                                    database='transcode',
                                    charset='utf8mb4')
        return db_connection

    def test(self):
        db_connection = self.get_connection()
        # 使用pandas读取数据
        sql_query = "SELECT * FROM device"
        df = pd.read_sql(sql_query, db_connection)
        # 关闭数据库连接
        db_connection.close()
        # 使用pandas DataFrame
        return df.to_dict(orient='records')    

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 50002)  # 服务器监听在0.0.0.0的port
    httpd = server_class(server_address, handler_class)
    print('Listening on port 50002...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

