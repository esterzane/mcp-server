from starlette.applications import Starlette
from starlette.routing import Mount
import uvicorn
import json

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

# Required by ChatGPT connectors / deep research
@mcp.tool()
def search(query: str) -> list[dict]:
    """
    Return exactly ONE content item of type 'text',
    where 'text' is a JSON-encoded string:
      {"results":[{"id","title","url"}...]}
    """
    payload = {"results": []}
    return [{"type": "text", "text": json.dumps(payload)}]

@mcp.tool()
def fetch(id: str) -> list[dict]:
    """
    Return exactly ONE content item of type 'text',
    where 'text' is the document/page content for the given id.
    """
    return [{"type": "text", "text": f"No content for id={id} (stub)."}]

# Optional extra tool (fine to keep)
@mcp.tool()
def ping(message: str) -> str:
    return f"pong: {message}"

app = Starlette(
    routes=[
        Mount("/sse", app=mcp.sse_app()),
    ]
)

if __name__ == "__main__":
    # IMPORTANT for ngrok: bind to 0.0.0.0, not 127.0.0.1
    uvicorn.run(app, host="0.0.0.0", port=8000)