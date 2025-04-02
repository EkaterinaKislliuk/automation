import unittest
import xmlrpc.client
from concurrent.futures import ThreadPoolExecutor

class TestRPCServerStress(unittest.TestCase):
    def setUp(self):
        self.proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    def test_stress(self):
        def send_command():
            return self.proxy.run_command("echo Stress Test")

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(send_command) for _ in range(100)]
            results = [future.result() for future in futures]

        for result in results:
            self.assertEqual(result["returncode"], 0)
            self.assertIn("Stress Test", result["stdout"])

if __name__ == "__main__":
    unittest.main()