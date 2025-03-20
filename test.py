# 客户端正确使用 POST 方法
import requests
secret_key = "gduifgashjb8t3961jhgsdghf"
response = requests.post("http://127.0.0.1:5000/list_tool", json={"server_name": "weather","secret_key":secret_key})
print(response.text)

response = requests.post("http://127.0.0.1:5000/call_tool", json={"server_name": "weather","tool_name":"get_alerts","args":{"state":"CA"},"secret_key":secret_key})
print(response.text)


response = requests.post("http://127.0.0.1:5000/list_server",json={"secret_key":secret_key})
print(response.text)

response = requests.post("http://127.0.0.1:5000/list_files",json={"secret_key":secret_key})
print(response.text)

response = requests.post(f"http://127.0.0.1:5000/get_download_link/{secret_key}/武士.png")
print(response.text)
