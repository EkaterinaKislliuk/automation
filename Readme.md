# SSH Connection Script

This Python script provides functionality to establish an SSH connection to a remote machine, execute commands, and retrieve the output. It uses the `paramiko` library for SSH communication and reads connection details from a YAML configuration file.

## Features

- Establish an SSH connection to a remote machine.
- Execute shell commands on the remote machine.
- Retrieve and display the output of executed commands.
- Check if the SSH session is active.
- Close the SSH session gracefully.

## Requirements

- Python 3.6 or higher
- Required Python libraries:
  - `paramiko`
  - `pyyaml`

You can install the required libraries using pip:

```bash
pip install paramiko pyyaml
