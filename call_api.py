import requests

def call_api(url, params=None):
    try:
        response = requests.get(url, params=params)
        # 如果需要发送 POST 请求，可以使用 requests.post(url, data=params) 替换上述行
        response.raise_for_status()  # 如果请求不成功，会抛出异常
        return response.json()  # 返回 JSON 格式的响应内容，如果返回的是其他格式可以使用 response.text
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 示例调用
api_url = 'https://devapi.qweather.com/v7/weather/now'
api_params = {'location': '101220101', 'key': '34e9ce9f92904c0d914511dc3ad2e646'}

result = call_api(api_url, api_params)
if result:
    print("接口调用成功！返回结果：")
    print(result)
