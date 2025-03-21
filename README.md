# mcp - client 项目详细使用文档

## 一、项目概述
`mcp - client` 项目旨在把本地的mcp-server通过flask暴露出来，用户自建内网穿透，实现coze/dify/fastgpt等平台与本地资源进行交互。

## 二、环境搭建

### 2.1 前置要求
请确保已安装 `uv` 工具（可参考 [官方文档](https://docs.astral.sh/uv/) 进行安装）。

### 2.2 创建项目目录
为项目创建一个新的目录，并进入该目录。以下命令展示了如何使用 `uv` 工具创建项目目录：
```bash
uv init project - name
cd project - name
```
这里的 `project - name` 是你为项目指定的名称，你可以根据实际情况进行修改。

### 2.3 创建并激活虚拟环境
使用 `uv` 工具创建虚拟环境，并激活它。虚拟环境可以帮助你隔离项目的依赖，避免不同项目之间的依赖冲突。
```bash
uv venv
.venv\Scripts\activate
```
在 Windows 系统中，激活虚拟环境的命令如上述所示。在 Linux 或 macOS 系统中，激活命令为：
```bash
source .venv/bin/activate
```

### 2.4 安装依赖
项目的依赖信息记录在 `pyproject.toml` 文件中，使用 `uv` 工具安装这些依赖：
```bash
uv install
```
此命令会自动读取 `pyproject.toml` 文件中的依赖信息，并将所需的库安装到虚拟环境中。

## 三、配置文件设置

### 3.1 服务器配置
在 `mcp_server.json` 文件中配置服务器信息。该文件定义了不同服务的描述、命令和参数。以下是一个示例：
```json:d:\project_python\MCP\mcp - client\mcp_server.json
{
    "mcpServers": {
        "weather": {
            "desc": "获取天气信息以及相关工具",
            "command": "uv",
            "args": [
                "--directory",
                "D:\\project_python\\MCP\\weather",
                "run",
                "weather.py"
            ]
        },
        "filesystem": {
            "desc": "文件管理",
            "command": "uv",
            "args": [
                "--directory",
                "D:\\project_python\\MCP\\mcp - server\\filesystem",
                "run",
                "main.py"
            ]
        }
    }
}
```
在这个示例中，定义了两个服务：`weather` 和 `filesystem`。你可以根据需要添加或修改服务配置。

### 3.2 环境变量配置

#### 3.2.1 从 `.env.example` 文件复制
在 GitHub 上项目通常会有 `.env.example` 文件，它是一个示例环境变量配置文件。你需要将其复制到项目根目录下并重命名为 `.env`：
```bash
cp .env.example .env
```

#### 3.2.2 填写环境变量
打开 `.env` 文件，根据项目实际需求填写环境变量的值。例如：
```plaintext:.env.example
ANTHROPIC_API_KEY = your_anthropic_api_key
SECRET_KEY = your_secret_key
```
将上述示例中的占位符替换为实际的值：
```plaintext:.env
ANTHROPIC_API_KEY = 123456
SECRET_KEY = gduifgashjb8t3961jhgsdghf
```

#### 3.2.3 忽略 `.env` 文件
为保护敏感信息，确保 `.gitignore` 文件中包含 `.env`，避免其被提交到版本控制系统。在 `.gitignore` 文件中添加：
```plaintext:.gitignore
.env
```

## 四、代码运行
启动服务器，运行 `server.py` 文件：
```bash
python server.py
```
运行该命令后，服务器将开始监听指定的端口，等待客户端的请求。

## 五、API 使用

### 5.1 列出指定服务器上的工具
发送 POST 请求到 `/list_tool` 端点，请求体示例：
```json
{
    "server_name": "weather",
    "secret_key": "gduifgashjb8t3961jhgsdghf"
}
```
这个请求会列出 `weather` 服务器上可用的工具。你可以使用 `curl` 或 Postman 等工具发送请求。例如，使用 `curl` 发送请求的命令如下：
```bash
curl -X POST -H "Content - Type: application/json" -d '{"server_name": "weather", "secret_key": "gduifgashjb8t3961jhgsdghf"}' http://localhost:5000/list_tool
```

### 5.2 调用指定服务器上的工具
发送 POST 请求到 `/call_tool` 端点，请求体示例：
```json
{
    "server_name": "weather",
    "tool_name": "get_weather",
    "args": {
        "city": "Beijing"
    },
    "secret_key": "gduifgashjb8t3961jhgsdghf"
}
```
这个请求会调用 `weather` 服务器上的 `get_weather` 工具，并传入参数 `city = Beijing`。使用 `curl` 发送请求的命令如下：
```bash
curl -X POST -H "Content - Type: application/json" -d '{"server_name": "weather", "tool_name": "get_weather", "args": {"city": "Beijing"}, "secret_key": "gduifgashjb8t3961jhgsdghf"}' http://localhost:5000/call_tool
```

### 5.3 列出所有服务器
发送 POST 请求到 `/list_server` 端点，请求体示例：
```json
{
    "secret_key": "gduifgashjb8t3961jhgsdghf"
}
```
使用 `curl` 发送请求的命令如下：
```bash
curl -X POST -H "Content - Type: application/json" -d '{"secret_key": "gduifgashjb8t3961jhgsdghf"}' http://localhost:5000/list_server
```

### 5.4 列出指定目录下的文件
发送 POST 请求到 `/list_files` 端点，请求体示例：
```json
{
    "secret_key": "gduifgashjb8t3961jhgsdghf"
}
```
使用 `curl` 发送请求的命令如下：
```bash
curl -X POST -H "Content - Type: application/json" -d '{"secret_key": "gduifgashjb8t3961jhgsdghf"}' http://localhost:5000/list_files
```

### 5.5 获取文件下载链接
发送 GET 请求到 `/get_download_link/<secret_key>/<filename>` 端点，例如：
```bash
curl http://localhost:5000/get_download_link/gduifgashjb8t3961jhgsdghf/example.txt
```
这个请求会返回 `example.txt` 文件的下载链接。

## 六、注意事项

### 6.1 服务器配置
请确保 `mcp_server.json` 文件中的路径和命令配置正确。如果路径或命令有误，可能会导致服务无法正常启动。

### 6.2 环境变量安全
请妥善保管 `.env` 文件中的环境变量，避免泄露。这些变量可能包含敏感信息，如 API 密钥等。

### 6.3 调试模式
在开发和测试过程中，可以使用 `app.run(debug = True, ssl_context = 'adhoc')` 开启调试模式。调试模式可以帮助你快速定位和解决问题，但在生产环境中不建议使用。

### 6.4 自签证书问题
由于项目使用了自签证书，在像 Coze 这样的云平台上可能会出现获取不到静态资源的情况。这是因为云平台通常会对证书的有效性进行严格验证，而自签证书没有经过受信任的证书颁发机构（CA）签名，所以会被认为是不安全的。

#### 解决方案建议
- **在本地开发环境**：继续使用自签证书和调试模式，因为本地环境对证书验证要求相对宽松。可使用 `app.run(debug = True, ssl_context = 'adhoc')` 开启调试模式。
- **在云平台部署**：考虑使用由受信任的证书颁发机构（如 Let's Encrypt）颁发的正式 SSL 证书。这样可以避免证书验证问题，确保云平台能够正常获取静态资源。你可以按照云平台的文档指引来配置和安装正式的 SSL 证书。
