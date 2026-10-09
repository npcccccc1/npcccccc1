# AnythingLLM MCP-Server MVP

MCP 协议版本：2026-07-28（由 mcp 2.0 SDK 自动协商），传输方式 Streamable HTTP，不使用 stdio。

功能：仅提供一个工具 `ask_first_workspace(question)`，向本机 AnythingLLM 第一个工作区提问，返回 AI 回答。

## 前置条件

1. 本地启动 AnythingLLM，访问地址 http://127.0.0.1:3001
2. 在 AnythingLLM 后台生成 API KEY 并写入 .env 文件
3. 运行环境为 Python 3.14（系统默认 `python` 是 2.7，须用 `py -3.14`）

## 安装依赖

    py -3.14 -m pip install -r requirements.txt

## 启动 MCP 服务

在项目根目录新开一个终端，前台运行：

    py -3.14 main.py

看到 `Uvicorn running on http://127.0.0.1:8080` 即启动成功，服务端点地址：http://127.0.0.1:8080/mcp 。

注意：HTTP 类型的 MCP 不会被 TRAE 自动拉起，必须先手动启动本服务，TRAE 才能连上。

如需后台运行（关掉终端窗口也不停，日志写入 mcp-server.log）：

    Start-Process -FilePath py -ArgumentList "-3.14","main.py" -WorkingDirectory $PWD -RedirectStandardOutput mcp-server.log -WindowStyle Hidden

## 停止 MCP 服务

- 前台运行时：在终端窗口按 `Ctrl + C`。
- 后台运行或找不到终端时，按端口查找进程并结束：

      netstat -ano | findstr "127.0.0.1:8080"
      taskkill /F /PID <最后一列的进程号>

  PowerShell 一行命令直接结束：

      Stop-Process -Id (Get-NetTCPConnection -LocalPort 8080 -State Listen).OwningProcess -Force

## 在 TRAE 中配置项目级 MCP

本服务使用 Streamable HTTP 传输，项目级配置文件为项目根目录的 `.trae/mcp.json`
（该文件受 TRAE 安全保护，需要手动创建，agent 无法代写入），内容如下：

    {
      "mcpServers": {
        "anythingllm-mcp-server": {
          "url": "http://127.0.0.1:8080/mcp"
        }
      }
    }

创建后还需在 TRAE 中开启开关：

1. 设置 > MCP
2. 打开「启用项目级 MCP」开关并在弹窗中确认
3. MCP 列表中出现 `anythingllm-mcp-server` 且状态正常即配置成功（连接前请确认服务已按上一节启动）

## 测试提问

新开聊天 session，输入任意问题，例如：

    帮我总结一下第一个工作区里的资料

注意：AI 回答基于工作区内已上传的文档，若第一个工作区没有文档，请先在 AnythingLLM 中上传。
