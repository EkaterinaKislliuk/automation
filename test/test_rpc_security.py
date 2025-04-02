import unittest
from rpc_server import run_command

class TestRPCServerSecurity(unittest.TestCase):
    def test_command_injection(self):
        response = run_command("echo safe && echo hacked")
        self.assertNotIn("hacked", response["stdout"])

    def test_restricted_commands(self):
        restricted_command = "rm -rf /" if os.name != "nt" else "del /Q *.*"
        response = run_command(restricted_command)
        self.assertNotEqual(response["returncode"], 0)

if __name__ == "__main__":
    unittest.main()