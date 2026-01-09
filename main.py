from starlette.applications import Starlette
from starlette.routing import Mount
import uvicorn

from mcp.server.fastmcp import FastMCP

# 1) Create the MCP server
mcp = FastMCP("My First MCP Server")

# 2) Define a simple tool the model can call
@mcp.tool()
def ping(message: str) -> str:
    """Return the same message (quick connectivity test)."""
    return f"pong: {message}"

# 3) Expose the MCP server over SSE at /sse
app = Starlette(
    routes=[
        Mount("/sse", app=mcp.sse_app("/sse")),
    ]
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)