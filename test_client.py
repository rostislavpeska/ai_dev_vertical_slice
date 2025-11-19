"""
Terminal Test Client for Vertical Slice PoC
Simple script to test the full pipeline
"""

import requests
import sys
import io

# Fix Unicode encoding for Windows terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def send_command(text: str, server_url: str = "http://localhost:8000"):
    """
    Send text command to FastAPI server
    
    Args:
        text: User command (e.g., "create a cube")
        server_url: FastAPI server URL
    """
    print(f"\n{'='*60}")
    print(f"📤 SENDING: {text}")
    print(f"{'='*60}")
    
    try:
        # Send POST request
        response = requests.post(
            f"{server_url}/run",
            json={"text": text},
            timeout=30
        )
        
        # Check status
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ SUCCESS:")
            print(f"   {result['result']}")
        else:
            print(f"\n❌ ERROR (HTTP {response.status_code}):")
            print(f"   {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ CONNECTION ERROR:")
        print(f"   Cannot connect to {server_url}")
        print(f"   Is the FastAPI server running?")
        print(f"   Run: python vertical_slice/backend/main.py")
        
    except requests.exceptions.Timeout:
        print(f"\n⏱️  TIMEOUT:")
        print(f"   Request took longer than 30 seconds")
        
    except Exception as e:
        print(f"\n❌ ERROR:")
        print(f"   {str(e)}")
    
    print(f"{'='*60}\n")


def interactive_mode():
    """Interactive mode - type commands one by one"""
    print("\n" + "="*60)
    print("🎯 BLENDIF VERTICAL SLICE - INTERACTIVE MODE")
    print("="*60)
    print("\nType commands (or 'quit' to exit):")
    print("Examples:")
    print("  - create a cube")
    print("  - create a sphere")
    print("  - import mesh from C:/path/to/model.obj")
    print("="*60 + "\n")
    
    while True:
        try:
            text = input("💬 You: ").strip()
            
            if not text:
                continue
                
            if text.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break
                
            send_command(text)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break


def main():
    """Main entry point"""
    # Check if command provided as argument
    if len(sys.argv) > 1:
        # Single command mode
        command = " ".join(sys.argv[1:])
        send_command(command)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()

