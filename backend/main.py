"""
FastAPI Backend for Vertical Slice PoC
Minimal implementation: User text -> Agent -> Router -> MCP
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.agent import run_agent  # Import real agent
from backend.router import route_tool  # Import real router

app = FastAPI(title="BlendIf Vertical Slice")

# Enable CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for PoC
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserRequest(BaseModel):
    text: str


class AgentResponse(BaseModel):
    result: str


@app.post("/run")
async def run_pipeline(request: UserRequest) -> AgentResponse:
    """
    Main pipeline endpoint:
    1. Receive user text
    2. Call LangGraph agent (placeholder)
    3. Call tool router (placeholder)
    4. Return result
    """
    user_text = request.text
    
    # PLACEHOLDER: Call LangGraph agent
    # Will return: { "tool": "create_cube", "args": {...} }
    agent_output = call_agent(user_text)
    
    # PLACEHOLDER: Call tool router
    # Routes to MCP based on tool name
    router_output = call_router(agent_output)
    
    return AgentResponse(result=router_output)


def call_agent(user_text: str) -> dict:
    """Call LangGraph agent - NOW IMPLEMENTED"""
    return run_agent(user_text)


def call_router(agent_output: dict) -> str:
    """Call tool router - NOW IMPLEMENTED"""
    return route_tool(agent_output)


@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "ok"}


@app.get("/")
async def serve_ui():
    """Serve the UI"""
    from fastapi.responses import FileResponse
    import os
    ui_path = os.path.join(os.path.dirname(__file__), "..", "ui", "index.html")
    return FileResponse(ui_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

