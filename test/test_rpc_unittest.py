import unittest
import os
from RPC_server import run_command

class TestRPCServer(unittest.TestCase):
    def test_run_command_success(self):
        response = run_command("echo Hello, World!")
        self.assertEqual(response["returncode"], 0)
        self.assertIn("Hello, World!", response["stdout"])

    def test_run_command_invalid(self):
        response = run_command("invalid_command")
        self.assertNotEqual(response["returncode"], 0)
        self.assertIn("not recognized" if os.name == "nt" else "not found", response["stderr"])

    def test_run_command_empty(self):
        response = run_command("")
        self.assertEqual(response["returncode"], 0)
        self.assertEqual(response["stdout"], "")

if __name__ == "__main__":
    unittest.main()