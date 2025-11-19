"""
Blender Socket Client
Connects to Blender addon on port 9876
"""

import socket
import json


class BlenderClient:
    """Simple socket client for Blender MCP addon"""
    
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
    
    def send_command(self, command_type: str, params: dict = None) -> dict:
        """
        Send command to Blender and get response
        
        Args:
            command_type: Type of command (e.g., "execute_code")
            params: Command parameters
        
        Returns:
            Response from Blender
        """
        if params is None:
            params = {}
        
        # Build command JSON
        command = {
            "type": command_type,
            "params": params
        }
        
        try:
            # Connect to Blender
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(10)  # 10 second timeout
                sock.connect((self.host, self.port))
                
                # Send command
                command_json = json.dumps(command)
                sock.sendall(command_json.encode('utf-8'))
                
                # Receive response
                response_data = b''
                while True:
                    chunk = sock.recv(8192)
                    if not chunk:
                        break
                    response_data += chunk
                    
                    # Try to parse (might be complete)
                    try:
                        response = json.loads(response_data.decode('utf-8'))
                        return response
                    except json.JSONDecodeError:
                        # Incomplete, keep receiving
                        continue
                
                # If we get here, connection closed
                if response_data:
                    return json.loads(response_data.decode('utf-8'))
                else:
                    return {"status": "error", "message": "No response from Blender"}
                    
        except socket.timeout:
            return {
                "status": "error",
                "message": "Connection timeout - is Blender running with MCP addon?"
            }
        except ConnectionRefusedError:
            return {
                "status": "error",
                "message": "Connection refused - is Blender running with MCP addon active?"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Connection error: {str(e)}"
            }
    
    def execute_code(self, code: str) -> dict:
        """Execute Python code in Blender"""
        return self.send_command("execute_code", {"code": code})
    
    def get_scene_info(self) -> dict:
        """Get information about current Blender scene"""
        return self.send_command("get_scene_info")


def create_cube(size: float = 2.0) -> str:
    """Create a cube in Blender"""
    client = BlenderClient()
    
    code = f"""
import bpy
bpy.ops.mesh.primitive_cube_add(size={size}, location=(0, 0, 0))
print("Cube created successfully")
"""
    
    response = client.execute_code(code)
    
    if response.get("status") == "success":
        return f"✅ Cube created in Blender (size={size})"
    else:
        return f"❌ Error: {response.get('message', 'Unknown error')}"


def create_sphere(radius: float = 1.0) -> str:
    """Create a sphere in Blender"""
    client = BlenderClient()
    
    code = f"""
import bpy
bpy.ops.mesh.primitive_uv_sphere_add(radius={radius}, location=(0, 0, 0))
print("Sphere created successfully")
"""
    
    response = client.execute_code(code)
    
    if response.get("status") == "success":
        return f"✅ Sphere created in Blender (radius={radius})"
    else:
        return f"❌ Error: {response.get('message', 'Unknown error')}"


def import_mesh(path: str) -> str:
    """Import a mesh file into Blender"""
    client = BlenderClient()
    
    # Support common formats
    if path.endswith('.obj'):
        code = f"""
import bpy
bpy.ops.wm.obj_import(filepath=r"{path}")
print("OBJ imported successfully")
"""
    elif path.endswith('.fbx'):
        code = f"""
import bpy
bpy.ops.import_scene.fbx(filepath=r"{path}")
print("FBX imported successfully")
"""
    else:
        return f"❌ Unsupported file format: {path}"
    
    response = client.execute_code(code)
    
    if response.get("status") == "success":
        return f"✅ Mesh imported: {path}"
    else:
        return f"❌ Error: {response.get('message', 'Unknown error')}"


def remesh_object(object_name: str) -> str:
    """Remesh an object using QRemeshify addon"""
    client = BlenderClient()
    
    code = f"""
import bpy

# Find object by name (case-insensitive search)
target_name = "{object_name}".lower()
found_obj = None

for obj in bpy.data.objects:
    if obj.name.lower().startswith(target_name):
        found_obj = obj
        break

if not found_obj:
    print(f"ERROR: Object not found: {object_name}")
else:
    # Select and make active
    bpy.ops.object.select_all(action='DESELECT')
    found_obj.select_set(True)
    bpy.context.view_layer.objects.active = found_obj
    
    # Call QRemeshify operator
    try:
        bpy.ops.qremeshify.remesh()
        print(f"SUCCESS: Remeshed {{found_obj.name}}")
    except Exception as e:
        print(f"ERROR: QRemeshify failed - {{str(e)}}")
"""
    
    response = client.execute_code(code)
    
    if response.get("status") == "success":
        result = response.get("result", {}).get("result", "")
        if "SUCCESS" in result:
            return f"✅ Object remeshed: {object_name}"
        elif "ERROR: Object not found" in result:
            return f"❌ Object '{object_name}' not found in scene"
        elif "ERROR: QRemeshify failed" in result:
            return f"❌ QRemeshify failed - is the addon installed?"
        else:
            return f"✅ Remesh operation completed for: {object_name}"
    else:
        return f"❌ Error: {response.get('message', 'Unknown error')}"
