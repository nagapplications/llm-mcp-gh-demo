from openai import OpenAI
import json
from mcp_client import get_tools, execute_tool, translate_tools_to_openai
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are an assistant that manages GitHub repositories using available tools.

When the user asks to:
- create or open a bug → use create_issue tool
- list or show issues → use list_issues tool

Always extract:
- repo name
- title (if creating issue)
- body (if creating issue)

If repo is not specified, assume 'question-service'.
"""

def process_prompt(prompt: str):
    # 1️⃣ Fetch tools from MCP server
    tools = get_tools()
    openai_tools = translate_tools_to_openai(tools)

    # 2️⃣ Ask LLM what tool to call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": prompt}],
        tools=openai_tools
    )

    # 3️⃣ Extract tool call
    tool_call = response.choices[0].message.tool_calls[0]
    tool_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    if "repo" not in arguments:
        arguments["repo"] = "question-service"


    # 4️⃣ Execute via MCP server
    result = execute_tool(tool_name, arguments)
    return result


if __name__ == "__main__":
    while True:
        user_input = input("\nEnter instruction for GitHub (or 'exit'): ")
        if user_input.lower() == "exit":
            break
        output = process_prompt(user_input)
        print("\n--- GitHub Response ---")
        print(json.dumps(output, indent=2))
