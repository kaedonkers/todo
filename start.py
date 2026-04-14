# ---
# created: 14 Apr 2026
# author: kaedonkers
# modified: 14 Apr 2026
# ---
# Start API server with optional GUI (FastAPI's Swagger UI)

import sys
import time
import subprocess
import webbrowser
import argparse

def start_server(host="127.0.0.1", port=8000, gui=True, server_wait_seconds=2):
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
    if gui:
        time.sleep(server_wait_seconds)
        print("Opening Swagger UI...")
        webbrowser.open(f"http://{host}:{port}/docs")
    # Keep the script running so the server stays up
    try:
        proc.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        proc.terminate()

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Start the FastAPI server, with optional UI")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    parser.add_argument("--gui", action="store_true", help="Start the server with the UI")
    parser.add_argument("--wait", type=float, default=2.0, help="Seconds to wait for server to start before opening UI")
    args = parser.parse_args()
    # Start the server with the specified options
    start_server(
        host=args.host,
        port=args.port,
        gui=args.gui,
        server_wait_seconds=args.wait
    )