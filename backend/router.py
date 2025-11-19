"""
Tool Router - Maps agent decisions to Blender actions
Simple if/else routing (no fancy abstractions)
"""

from backend.mcp_client import create_cube, create_sphere, import_mesh, remesh_object


def route_tool(tool_call: dict) -> str:
    """
    Route agent's tool call to appropriate function
    
    Args:
        tool_call: Dict from agent with {"tool": "...", "args": {...}}
    
    Returns:
        Result string from execution
    """
    tool_name = tool_call.get("tool")
    args = tool_call.get("args", {})
    
    # Handle invalid commands
    if tool_name == "invalid":
        message = tool_call.get("message", "Invalid command")
        return f"❌ {message}"
    
    # Handle errors from agent
    if tool_name == "error":
        message = tool_call.get("message", "Unknown error")
        return f"❌ Agent error: {message}"
    
    # Route to Blender functions
    if tool_name == "create_cube":
        size = args.get("size", 2.0)
        return create_cube(size=size)
    
    elif tool_name == "create_sphere":
        radius = args.get("radius", 1.0)
        return create_sphere(radius=radius)
    
    elif tool_name == "import_mesh":
        path = args.get("path")
        if not path:
            return "❌ Error: import_mesh requires 'path' argument"
        return import_mesh(path=path)
    
    elif tool_name == "remesh_object":
        object_name = args.get("object_name")
        if not object_name:
            return "❌ Error: remesh_object requires 'object_name' argument"
        return remesh_object(object_name=object_name)
    
    else:
        return f"❌ Unknown tool: {tool_name}"

