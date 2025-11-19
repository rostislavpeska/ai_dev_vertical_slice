# AI-Driven 3D Workflow Orchestrator - Vertical Slice

**School Project: AI Engineer Course**  
**November 2025**

---

## 📋 Project Overview

This vertical slice demonstrates an AI-powered pipeline that translates natural language commands into Blender 3D operations. The system uses GPT-4 to understand user intent and routes commands to a 3D modeling application.

### Architecture

```
User Input (Web UI / Terminal)
    ↓
FastAPI Backend (REST API)
    ↓
LangGraph Agent (GPT-4o - Single Node)
    ↓
Tool Router (Python if/else)
    ↓
Blender MCP Socket Client (port 9876)
    ↓
Blender 3D Application
```

---

## 🎯 Key Features

- **Natural Language Processing**: Converts plain English to structured commands
- **Simple Agent Architecture**: Single-node LangGraph for command interpretation
- **Tool Routing**: Maps AI decisions to specific Blender operations
- **Socket Communication**: Direct integration with Blender via TCP socket
- **Dual Interface**: Web UI and terminal client for testing

---

## 🛠 Technical Stack

- **Backend**: FastAPI (Python)
- **AI Agent**: LangGraph + OpenAI GPT-4o
- **3D Software**: Blender 3.0+ with MCP addon
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Communication**: REST API + TCP Sockets

---

## 📁 Project Structure

```
vertical_slice/
├── backend/
│   ├── main.py          # FastAPI server + endpoints
│   ├── agent.py         # LangGraph agent (single node)
│   ├── router.py        # Tool routing logic
│   └── mcp_client.py    # Blender socket client
├── ui/
│   └── index.html       # Web interface
├── test_client.py       # Terminal test client
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

---

## 🚀 Installation & Setup

### Prerequisites

1. **Python 3.10+**
2. **Blender 3.0+** 
3. **OpenAI API Key**
4. **Blender Addons:**
   - Blender MCP (for socket communication)
   - QRemeshify (for topology optimization)

### Step 1: Install Dependencies

```bash
cd vertical_slice
pip install -r requirements.txt
```

### Step 2: Configure Environment

Create `.env` file in project root:

```env
OPENAI_API_KEY=your-openai-api-key-here
BLENDER_HOST=localhost
BLENDER_PORT=9876
```

### Step 3: Install Blender Addons

**A) Blender MCP Addon:**
1. Download: `../repos/blender-mcp/addon.py`
2. Open Blender → Edit → Preferences → Add-ons
3. Click "Install..." → Select `addon.py`
4. Enable "Interface: Blender MCP"

**B) QRemeshify Addon:**
1. Download from: https://github.com/ksami/QRemeshify/releases
2. Open Blender → Edit → Preferences → Add-ons
3. Click dropdown arrow (top right) → "Install from Disk..."
4. Select downloaded zip file
5. Enable "QRemeshify"

### Step 4: Start Blender Server

1. In Blender, press `N` (opens sidebar)
2. Find "BlenderMCP" tab
3. Click "Connect to Claude" button
4. ✅ Server running on port 9876

---

## ▶️ Running the Application

### Option 1: Web UI (Recommended)

**Terminal 1 - Start Backend:**
```bash
cd vertical_slice
python -m backend.main
```

**Browser:**
Open: `http://localhost:8000`

Type commands like:
- "create a cube"
- "create a sphere"

---

### Option 2: Terminal Client

**Terminal 1 - Start Backend:**
```bash
python -m backend.main
```

**Terminal 2 - Send Commands:**
```bash
# Interactive mode
python test_client.py

# Single command
python test_client.py "create a cube"
```

---

## 🎮 Supported Commands

| Command | Description | Example |
|---------|-------------|---------|
| `create a cube` | Creates a 2x2 cube | Default size |
| `create a sphere` | Creates a UV sphere | Default radius 1.0 |
| `import mesh from [path]` | Imports OBJ/FBX file | Full file path required |
| `remesh [object]` | Remeshes object to clean quads | "remesh suzanne" |

---

## 🏗️ How It Works

### 1. User Input
User types natural language command in UI or terminal

### 2. FastAPI Endpoint
```python
POST /run
Body: {"text": "create a cube"}
```

### 3. LangGraph Agent
Single node processes input with GPT-4o:
- Parses user intent
- Extracts parameters
- Returns structured JSON: `{"tool": "create_cube", "args": {"size": 2.0}}`

### 4. Tool Router
Simple Python function:
```python
if tool_name == "create_cube":
    return create_cube(size=args.get("size", 2.0))
```

### 5. MCP Socket Client
Sends JSON command to Blender:
```json
{
  "type": "execute_code",
  "params": {
    "code": "import bpy\nbpy.ops.mesh.primitive_cube_add(size=2.0)"
  }
}
```

### 6. Blender Execution
Blender MCP addon receives command, executes, returns status

---

## 🧪 Testing

### Test 1: Basic Cube Creation
```
Input: "create a cube"
Expected: Cube appears in Blender
```

### Test 2: Sphere Creation
```
Input: "create a sphere"
Expected: Sphere appears in Blender
```

### Test 3: Invalid Command Handling
```
Input: "what's the weather?"
Expected: Error message - "Please provide a Blender command"
```

---

## 🐛 Troubleshooting

### "Connection refused"
- ✅ Check Blender is running
- ✅ Check MCP addon is active
- ✅ Click "Connect to Claude" in Blender sidebar

### "OPENAI_API_KEY not found"
- ✅ Check `.env` file exists in project root
- ✅ Verify API key starts with `sk-`
- ✅ Restart server after creating `.env` file

### "Failed to fetch" (Web UI)
- ✅ Check FastAPI server is running
- ✅ Access UI via `http://localhost:8000` not `file://`

### Virtual Environment Issues
- ✅ Deactivate venv: `deactivate`
- ✅ Use system Python for this project

---

## 🔧 Debugging Cheatsheet

### Port 8000 Already in Use
```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill specific process (replace PID with number from above)
taskkill /F /PID <PID>

# Kill all Python processes (nuclear option)
taskkill /F /IM python.exe
```

### Server Won't Start
```powershell
# 1. Check if port is free
netstat -ano | findstr :8000

# 2. Kill existing process
taskkill /F /PID <PID>

# 3. Make sure you're in correct directory
cd C:\Users\TIGO\Desktop\vertical_slice

# 4. Start server
python -m backend.main
```

### Changes Not Working
```powershell
# Always restart server after code changes!
# 1. Stop server: Ctrl+C
# 2. Start again: python -m backend.main
```

### Wrong Virtual Environment
```powershell
# Check if in venv (prompt shows (.venv))
# If yes, deactivate:
deactivate

# Then run normally:
python -m backend.main
```

### Quick Reset (When Everything is Broken)
```powershell
# Kill all Python, restart fresh
taskkill /F /IM python.exe; cd C:\Users\TIGO\Desktop\vertical_slice; python -m backend.main
```

---

## 📊 Design Decisions

### Why Single-Node LangGraph?
- **Simplicity**: Easier to debug and understand
- **Sufficient**: No complex reasoning required for command parsing
- **Performance**: Lower latency than multi-node graphs

### Why Socket Connection?
- **Direct**: No middleware or protocol overhead
- **Real-time**: Immediate feedback from Blender
- **Existing**: Leverages existing Blender MCP addon

### Why Minimal UI?
- **PoC Focus**: Demonstrates concept, not production polish
- **No Build Tools**: Single HTML file, easy to run
- **Time Efficient**: Built in 30 minutes

---

## 🔮 Future Enhancements

- Add more tools (lights, cameras, materials)
- Implement conversation memory
- Add 3D model generation (Trellis integration)
- Support for complex multi-step workflows
- Error recovery and retry logic
- Asset library browser

---

## 📝 Key Learnings

1. **LangGraph Architecture**: Single-node agents are sufficient for simple routing tasks
2. **Socket Communication**: Direct integration is faster than HTTP for local apps
3. **Error Handling**: Clear error messages are critical for debugging
4. **Dual Interfaces**: Terminal + Web UI provides flexibility during development

---

## 🎓 Academic Context

**Course**: AI Engineer  
**Focus**: Practical AI agent implementation  
**Scope**: Vertical slice demonstrating core pipeline  
**Time**: Completed in one evening (~6 hours)  
**Lines of Code**: ~600 (excluding UI components)

---

## 📄 License

Educational project - free to use and modify.

---

## 🙏 Acknowledgments

- **Blender MCP**: Open-source addon for Blender integration
- **LangChain/LangGraph**: Agent framework
- **OpenAI**: GPT-4o API
- **FastAPI**: Modern Python web framework

---

**Built with focus on clarity, simplicity, and demonstrable results.**
