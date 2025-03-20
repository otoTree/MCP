from flask import Flask, request, jsonify,send_file
from client import MCPClient
import asyncio
import json
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
def check(token):
    secret_key = os.getenv('SECRET_KEY')
    if token == secret_key:
        return True
    else:
        return False
    

async def get_tool(server_name):
    """获取指定服务器上的工具列表"""
    async with MCPClient(server_name=server_name) as client:
        return client.tools

async def call_tool(tool_name, server_name, args: dict):
    """调用指定服务器上的工具"""
    async with MCPClient(server_name=server_name) as client:
        result = await client.call(tool_name, args)
        return result

@app.route('/list_tool', methods=['POST'])
async def list_tool():
    """列出指定服务器上的工具"""
    data = request.get_json()
    server_name = data.get("server_name")

    secret_key = data.get("secret_key")

    if check(secret_key):
        pass
    else:
        return jsonify({"error": "secret_key is incorrect"}), 413

    if not server_name:
        return jsonify({"error": "Missing 'server_name' parameter"}), 400

    try:
        tools = await get_tool(server_name)
        # Convert each Tool object to a dictionary
        tools_dict = [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.inputSchema
            }
            for tool in tools
        ]
        return jsonify({"tools": tools_dict}), 200
    except Exception as e:
        print(f"Error listing tools: {e}")
        return jsonify({"error": "Failed to list tools"}), 500

@app.route('/call_tool', methods=['POST'])
async def call_tool_route():
    """调用工具并返回结果"""
    data = request.get_json()
    server_name = data.get("server_name")
    tool_name = data.get("tool_name")
    args = data.get("args", {})

    secret_key = data.get("secret_key")

    if check(secret_key):
        pass
    else:
        return jsonify({"error": "secret_key is incorrect"}), 413
    

    if not server_name or not tool_name:
        return jsonify({"error": "Missing 'server_name' or 'tool_name' parameter"}), 400

    try:
        result = await call_tool(server_name=server_name, tool_name=tool_name, args=args)
        # Return a consistent response format
        return jsonify({
            "status": "success",
            "tool_name": tool_name,
            "result": result.json()
        }), 200
    except Exception as e:
        print(f"Error calling tool: {e}")
        return jsonify({
            "status": "error",
            "error": "Tool call failed",
            "details": str(e)
        }), 500

@app.route('/list_server', methods=['POST'])
async def list_server():
    data = request.get_json()
    secret_key = data.get("secret_key")

    if check(secret_key):
        pass
    else:
        return jsonify({"error": "secret_key is incorrect"}), 413
    
    with open("mcp_server.json", "r", encoding='utf-8') as f:
        servers = f.read() 
    return jsonify({"server": servers}), 200

@app.route('/list_files', methods=['POST'])
async def list_files():
    data = request.get_json()
    secret_key = data.get("secret_key")

    if check(secret_key):
        pass
    else:
        return jsonify({"error": "secret_key is incorrect"}), 413
    
    # 目录路径
    directory = 'static'
    # 检查目录是否存在
    if not os.path.exists(directory):
        return "Directory not found", 404
    # 获取目录下的文件列表
    files = os.listdir(directory)
    return jsonify({"files": files})

@app.route('/get_download_link/<secret_key>/<filename>', methods=['POST'])
async def get_download_link(secret_key,filename):
    
    if check(secret_key):
        pass
    else:
        return jsonify({"error": "secret_key is incorrect"}), 413
    
    # 文件路径
    file_path = os.path.join('static', filename)
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
