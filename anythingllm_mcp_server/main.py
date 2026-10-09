"""AnythingLLM MCP Server (MVP)

唯一功能：向本机 AnythingLLM 的第一个工作区提问，返回 AI 回答。
MCP 2026-07-28 协议，Streamable HTTP 传输，端点 /mcp。
"""
import os

import httpx
from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer

load_dotenv()

BASE_URL = os.getenv("ANYTHINGLLM_URL", "http://127.0.0.1:3001").rstrip("/")
API_KEY = os.getenv("ANYTHINGLLM_API_KEY", "")
HOST = os.getenv("MCP_HTTP_HOST", "127.0.0.1")
PORT = int(os.getenv("MCP_HTTP_PORT", "8080"))

mcp = MCPServer("anythingllm-mcp-server")


@mcp.tool()
async def ask_first_workspace(question: str) -> str:
    """向 AnythingLLM 的第一个工作区提问，返回 AI 基于该工作区内容给出的回答。

    参数:
        question: 要提问的问题。
    """
    async with httpx.AsyncClient(
        base_url=BASE_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=60,
    ) as client:
        resp = await client.get("/api/v1/workspaces")
        resp.raise_for_status()
        workspaces = resp.json().get("workspaces", [])
        if not workspaces:
            return "错误：AnythingLLM 中不存在任何工作区"

        slug = workspaces[0]["slug"]
        resp = await client.post(
            f"/api/v1/workspace/{slug}/chat",
            json={"message": question},
        )
        resp.raise_for_status()
        answer = resp.json().get("textResponse")
        return answer or "错误：AI 未返回文本内容"


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host=HOST, port=PORT)
