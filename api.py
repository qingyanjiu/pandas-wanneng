from flask import Flask, request
from flask_cors import CORS
import requests
app = Flask(__name__)
# 允许所有域名访问
CORS(app,resources=r"/*", supports_credentials=True, content_types=['application/json'])
@app.route('/getWeather', methods=['POST'])
def getWeather():
    # 获取天气url
    data = request.json
    print(data,'ppppppppppppp')
    if not data or 'url' not in data:
        # 如果请求数据不合法，返回错误响应
        print({'error': 'Invalid request data'}, 400)
    print(data['url'])
    weatherUrl =data['url']

    # 发送HTTP请求获取天气数据
    response = requests.get(weatherUrl)
    # 检查响应状态码
    if response.status_code == 200:
        # 解析JSON格式的响应内容
        weather_data = response.json()
        return weather_data
    else:
        # 如果请求失败，打印错误信息
        print('Failed to retrieve weather data:', response.status_code)
        return None
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
