# ---
# created: 14 Apr 2026
# author: kaedonkers
# modified: 14 Apr 2026
# ---
# Start API server with optional GUI

import sys
import time
import subprocess
import webbrowser
import argparse

def start_server(host="127.0.0.1", port=8000, gui=True, docs=True, server_wait_seconds=2):
    # Start uvicorn in a subprocess
    proc = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "app.main:app", 
        "--reload", 
        "--host", host, 
        "--port", str(port)
    ])
    print("Server starting...")
    # (Optional): Open the docs URL in browser, after waiting for the server to start
    if gui or docs:
        time.sleep(server_wait_seconds)
        print(f"Waiting {server_wait_seconds} seconds for server to start...")
    if gui:
        print("Opening Swagger UI...")
        webbrowser.open(f"http://{host}:{port}/docs")
    if docs:
        print("Opening ReDoc UI...")
        webbrowser.open(f"http://{host}:{port}/redoc")
    # Keep the script running so the server stays up
    try:
        proc.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        proc.terminate()

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Start the todo server, with optional UI")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    parser.add_argument("--gui", action="store_true", help="Open server GUI in the browser")
    parser.add_argument("--docs", action="store_true", help="Open server documentation in the browser")
    parser.add_argument("--wait", type=float, default=2.0, help="Seconds to wait for server to start before opening browser")
    args = parser.parse_args()
    # Start the server with the specified options
    start_server(
        host=args.host,
        port=args.port,
        gui=args.gui,
        docs=args.docs,
        server_wait_seconds=args.wait,
    )