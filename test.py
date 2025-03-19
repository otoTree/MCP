# 客户端正确使用 POST 方法
import requests
response = requests.post("http://127.0.0.1:5000/list_tool", json={"server_name": "weather"})
print(response.text)

response = requests.post("http://127.0.0.1:5000/call_tool", json={"server_name": "weather","tool_name":"get_alerts","args":{"state":"CA"}})
print(response.text)


response = requests.post("http://127.0.0.1:5000/list_server",)
print(response.text)
