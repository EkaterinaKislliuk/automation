from xmlrpc.server import SimpleXMLRPCServer
import subprocess

def run_command(command):
    """
    Execute a command on the command line and return the output.
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    """
    Set up and start the RPC server.
    """
    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    print("RPC server is running on port 8000...")

    # Register the function to run commands
    server.register_function(run_command, "run_command")

    # Start the server
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server.")
        server.server_close()

if __name__ == "__main__":
    main()