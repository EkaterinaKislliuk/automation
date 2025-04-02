import paramiko
import yaml
import argparse
class SSHConnect:
    def __init__(self, config_file):
        """
        Initialize the SSHConnect class with configuration file.
        """
        self.config_file = config_file
        self.ssh_client = None
        self.shell = None
        self.buffer = ""

    def load_config(self):
        """
        Load the YAML configuration file for SSH credentials.
        """
        with open(self.config_file, 'r') as file:
            config = yaml.safe_load(file)
        return config

    def connect(self):
        """
        Setup SSH connection with the remote machine.
        """
        try:
            config = self.load_config()
            hostname = config.get('hostname')
            port     = config.get('port')
            username = config.get('username')
            password = config.get('password')

            if not all([hostname, port, username, password]):
                raise ValueError("Missing hostname, username, or password in the configuration file.")

            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.load_system_host_keys()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname,port=port, username=username, password=password)
            self.shell = self.ssh_client.invoke_shell()
        except paramiko.AuthenticationException:
            raise ConnectionError("Authentication failed, please verify your credentials.")
        except paramiko.SSHException as ssh_exception:
            raise ConnectionError(f"Unable to establish SSH connection: {ssh_exception}")
        except Exception as e:
            raise ConnectionError(f"An error occurred while connecting: {e}")


    def send_cmd(self, command):
        """
        Send a command to the remote machine.
        """
        if self.shell:
            self.shell.send(command + '\n')
        else:
            raise ConnectionError("Shell is not active. Please connect first.")

    def read(self):
        """
        Check if the session is active and read the buffer.
        """
        if self.shell and self.shell.recv_ready():
            self.buffer = self.shell.recv(1024).decode('utf-8')
            return self.buffer
        else:
            return "No data received or shell is not active."

    def close(self):
        """
        Close the SSH client session.
        """
        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None
            self.shell = None
        else:
            raise ConnectionError("SSH client is not connected.")
        
    def is_active(self):
        """
        Check if the SSH session is active.
        """
        return self.ssh_client is not None and self.ssh_client.get_transport() is not None and self.ssh_client.get_transport().is_active()

    
    @classmethod
    def create_client(cls, config_file):
        """
        Class method to create and return an SSHClient instance.
        """
        instance = cls(config_file)
        instance.connect()
        return instance.ssh_client

def main():
    """
    Main method to run the module as a script.
    """
    parser = argparse.ArgumentParser(description="SSH Connection Script")
    parser.add_argument("config_file", help="Path to the YAML configuration file")
    args = parser.parse_args()

    ssh = SSHConnect(args.config_file)
    try:
        ssh.connect()
        print("Connection established.")
        ssh.send_cmd("ls")
        print("Command output:")
        print(ssh.read())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ssh.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
    
