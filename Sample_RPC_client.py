import os

def main():
    # Connect to the RPC server
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
    
    # Define a command based on the operating system
    if os.name == "nt":  # Windows
        command = "dir"  # Windows equivalent of 'ls'
    else:  # Unix/Linux/Mac
        command = "ls"
    
    # Send the command to the RPC server
    response = proxy.run_command(command)
    
    # Print the response
    print("Command Output:")
    print(response.get("stdout", ""))
    print("Error Output:")
    print(response.get("stderr", ""))
    print("Return Code:", response.get("returncode", "Unknown"))

if __name__ == "__main__":
    main()