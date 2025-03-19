from flask import Flask, request, jsonify
from client import MCPClient
import asyncio
import json
app = Flask(__name__)

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
    with open("mcp_server.json", "r", encoding='utf-8') as f:
        servers = f.read() 
    return jsonify({"server": servers}), 200


if __name__ == '__main__':
    app.run(debug=True)
