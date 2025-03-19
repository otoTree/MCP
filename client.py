import asyncio
import json
from contextlib import AsyncExitStack
from typing import List, Dict, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    """MCP客户端核心类，管理服务器连接和会话生命周期"""
    
    def __init__(self, config_path: str = 'mcp_server.json', server_name: str = 'weather'):
        """
        初始化客户端实例
        :param config_path: 配置文件路径
        :param server_name: 要连接的服务器名称
        """
        self._config = self._load_config(config_path)
        self.server_name = server_name
        self._exit_stack: Optional[AsyncExitStack] = None
        self.session: Optional[ClientSession] = None
        self.tools = {}
    
    @staticmethod
    def _load_config(config_path: str) -> Dict:
        """加载JSON配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"配置加载失败: {str(e)}") from e

    async def __aenter__(self):
        """异步上下文管理器入口"""
        self._exit_stack = AsyncExitStack()
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口，负责资源清理"""
        if self._exit_stack:
            await self._exit_stack.aclose()

    async def _connect(self):
        """建立服务器连接的核心方法"""
        # 获取服务器配置
        server_config = self._config['mcpServers'][self.server_name]
        
        # 初始化服务器参数
        server_params = StdioServerParameters(
            command=server_config["command"],
            args=server_config["args"],
            env=None
        )
        
        # 建立标准IO连接
        stdio, writer = await self._exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        
        # 初始化客户端会话
        self.session = await self._exit_stack.enter_async_context(
            ClientSession(stdio, writer)
        )
        
        # 执行会话初始化
        await self.session.initialize()
        
        # 获取工具列表
        response = await self.session.list_tools()

        self.tools = response.tools

    def get_server_config(self, key: str) -> str:
        """获取指定服务器配置项"""
        return self._config['mcpServers'][self.server_name].get(key, "")

    async def reconnect(self):
        
        """重新连接服务器"""
        if self._exit_stack:
            await self._exit_stack.aclose()
        self._exit_stack = AsyncExitStack()
        await self._connect()

    #工具调用
    async def call(self,name,args):
        return await self.session.call_tool(name,args)


'''
if __name__ == "__main__":
    async def main():
        """使用示例"""
        async with MCPClient() as client:
            print(f"已连接服务器: {client.server_name}")
            print("可用工具列表:", client.tools)
            print("工具调用： ",await client.call(client.tools[0].name,{"state":"CA"}))
    
    asyncio.run(main())'''