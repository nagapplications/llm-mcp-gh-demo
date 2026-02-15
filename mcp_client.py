import requests
import json

MCP_SERVER_URL = "http://127.0.0.1:8001"


# ----------------------------
# Fetch available tools
# ----------------------------
def get_tools():
    response = requests.get(f"{MCP_SERVER_URL}/tools")
    response.raise_for_status()
    return response.json()


# ----------------------------
# Execute a tool by name
# ----------------------------
def execute_tool(tool_name, arguments: dict):
    response = requests.post(f"{MCP_SERVER_URL}/execute/{tool_name}", json=arguments)
    response.raise_for_status()
    return response.json()


# ----------------------------
# Translate MCP server tools -> OpenAI function format
# ----------------------------
def translate_tools_to_openai(tools):
    """
    MCP server returns custom schema:
    {
        "tool_name": "...",
        "tool_description": "...",
        "parameters": { "repo": "string", "title": "string" ... }
    }
    """
    openai_tools = []
    for t in tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": t["tool_name"],
                "description": t["tool_description"],
                "parameters": {
                    "type": "object",
                    "properties": {k: {"type": "string"} for k in t["parameters"].keys()},
                    "required": list(t["parameters"].keys())
                }
            }
        })
    return openai_tools
