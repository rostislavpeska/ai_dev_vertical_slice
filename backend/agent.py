"""
LangGraph Mini Agent - Single Node
Converts user text into structured tool calls for Blender
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()


class AgentState(TypedDict):
    """Simple state: input text and output tool call"""
    user_text: str
    tool_call: dict


def create_llm():
    """Create OpenAI client with API key from .env"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file!")
    
    return ChatOpenAI(
        model="gpt-4o",
        api_key=api_key,
        temperature=0  # Deterministic responses
    )


def planner_node(state: AgentState) -> AgentState:
    """
    Single LangGraph node: 'planner'
    Takes user text, returns structured tool call
    """
    user_text = state["user_text"]
    llm = create_llm()
    
    # System prompt: Only accept Blender commands (Option 1)
    system_prompt = """You are a Blender command router.

Your job: Convert user commands into structured tool calls.

Available tools:
- create_cube: Creates a cube in Blender. Args: {"size": float (optional)}
- create_sphere: Creates a sphere. Args: {"radius": float (optional)}
- import_mesh: Imports a mesh file. Args: {"path": string (required)}
- remesh_object: Remeshes an object to clean quad topology. Args: {"object_name": string (required)}

Response format (JSON only):
{"tool": "tool_name", "args": {...}}

If user asks something NOT related to Blender commands, respond:
{"tool": "invalid", "message": "Please provide a Blender command like 'create cube' or 'remesh suzanne'"}

Examples:
User: "create a cube" -> {"tool": "create_cube", "args": {}}
User: "import mesh from Desktop/model.obj" -> {"tool": "import_mesh", "args": {"path": "Desktop/model.obj"}}
User: "remesh suzanne" -> {"tool": "remesh_object", "args": {"object_name": "suzanne"}}
User: "clean up topology of cube" -> {"tool": "remesh_object", "args": {"object_name": "cube"}}
User: "how are you?" -> {"tool": "invalid", "message": "Please provide a Blender command"}
"""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_text)
    ]
    
    # Call GPT-4
    response = llm.invoke(messages)
    
    # Parse JSON response
    try:
        tool_call = json.loads(response.content)
    except json.JSONDecodeError:
        tool_call = {
            "tool": "error",
            "message": f"Agent returned invalid JSON: {response.content}"
        }
    
    state["tool_call"] = tool_call
    return state


def build_graph():
    """Build the LangGraph with single node"""
    workflow = StateGraph(AgentState)
    
    # Add single node: planner
    workflow.add_node("planner", planner_node)
    
    # Set entry point
    workflow.set_entry_point("planner")
    
    # End after planner (no loops)
    workflow.add_edge("planner", END)
    
    return workflow.compile()


def run_agent(user_text: str) -> dict:
    """
    Main entry point for agent
    Called from main.py
    """
    graph = build_graph()
    
    # Run graph with initial state
    result = graph.invoke({
        "user_text": user_text,
        "tool_call": {}
    })
    
    return result["tool_call"]

