from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = "nagapplications"

print("GITHUB_TOKEN:", GITHUB_TOKEN)
print("Token length:", len(GITHUB_TOKEN))


app = FastAPI(title="Demo MCP Server")

# ----------------------------
# Tool Input Schemas
# ----------------------------

class CreateIssueInput(BaseModel):
    repo: str
    title: str
    body: str

class ListIssuesInput(BaseModel):
    repo: str


# ----------------------------
# Tool Discovery Endpoint
# ----------------------------

@app.get("/tools")
def list_tools():
    return [
        {
            "tool_name": "create_issue",
            "tool_description": "Create a new issue in a GitHub repository",
            "parameters": {
                "repo": "string",
                "title": "string",
                "body": "string"
            }
        },
        {
            "tool_name": "list_issues",
            "tool_description": "List open issues from a GitHub repository",
            "parameters": {
                "repo": "string"
            }
        }
    ]


# ----------------------------
# Tool Execution: Create Issue
# ----------------------------

@app.post("/execute/create_issue")
def create_issue(data: CreateIssueInput):

    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{data.repo}/issues"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "title": data.title,
        "body": data.body
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


# ----------------------------
# Tool Execution: List Issues
# ----------------------------

@app.post("/execute/list_issues")
def list_issues(data: ListIssuesInput):

    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{data.repo}/issues"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    # Return simplified output for demo clarity
    issues = response.json()
    simplified = [
        {
            "number": issue["number"],
            "title": issue["title"],
            "state": issue["state"]
        }
        for issue in issues
    ]

    return simplified
