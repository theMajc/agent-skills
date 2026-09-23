#!/usr/bin/env python3
"""
Unit and integration tests for mock-upstream-api scaffolding and templates.
"""

import http.client
import json
import os
import subprocess
import time
import unittest
import urllib.request
import urllib.error

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SKILL_ROOT = os.path.join(REPO_ROOT, "skills", "mock-upstream-api")
SCAFFOLD_SCRIPT = os.path.join(SKILL_ROOT, "scripts", "scaffold_mock.py")

class TestMockApiScaffold(unittest.TestCase):
    def test_scaffold_cli_generation_node_builtin(self):
        cmd = [
            "python3", SCAFFOLD_SCRIPT,
            "--entity", "user",
            "--fields", "id:string,name:string,email:string,role:string,createdAt:datetime",
            "--count", "25",
            "--port", "4999",
            "--flavor", "node-builtin"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        self.assertIn("Zero-dependency Node.js Upstream Mock Server", result.stdout)
        self.assertIn("user", result.stdout)
        self.assertIn("RATE_LIMIT_MAX", result.stdout)
        self.assertIn("X-RateLimit-Limit", result.stdout)
        self.assertIn("Retry-After", result.stdout)

    def test_scaffold_cli_generation_express(self):
        cmd = [
            "python3", SCAFFOLD_SCRIPT,
            "--entity", "order",
            "--fields", "id:string,amount:number,status:string",
            "--count", "10",
            "--port", "4998",
            "--flavor", "express-js"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        self.assertIn("Express.js Upstream Mock Server", result.stdout)
        self.assertIn("order", result.stdout)

    def test_scaffold_cli_generation_fastapi(self):
        cmd = [
            "python3", SCAFFOLD_SCRIPT,
            "--entity", "product",
            "--fields", "id:string,price:number,name:string",
            "--count", "15",
            "--flavor", "fastapi"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        self.assertIn("FastAPI", result.stdout)
        self.assertIn("RATE_LIMIT_MAX", result.stdout)

    def test_live_node_builtin_server(self):
        test_file = "/tmp/test_mock_server.mjs"
        cmd = [
            "python3", SCAFFOLD_SCRIPT,
            "--entity", "transaction",
            "--fields", "id:string,amount:number,status:string,createdAt:datetime",
            "--count", "30",
            "--port", "5123",
            "--rate-limit", "5",
            "--rate-window", "5",
            "--output", test_file
        ]
        subprocess.run(cmd, check=True)
        self.assertTrue(os.path.exists(test_file))

        # Start server process
        server_proc = subprocess.Popen(["node", test_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(0.5)

        try:
            # 1. Health check
            req = urllib.request.Request("http://127.0.0.1:5123/health")
            with urllib.request.urlopen(req) as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode())
                self.assertEqual(data["status"], "healthy")

            # 2. Paginated collection - Page 1
            req = urllib.request.Request("http://127.0.0.1:5123/api/transactions?page=1&limit=10")
            with urllib.request.urlopen(req) as resp:
                self.assertEqual(resp.status, 200)
                self.assertEqual(resp.headers.get("X-Total-Count"), "30")
                self.assertEqual(resp.headers.get("X-Has-More"), "true")
                data = json.loads(resp.read().decode())
                self.assertEqual(len(data["data"]), 10)
                self.assertEqual(data["pagination"]["total"], 30)
                self.assertEqual(data["pagination"]["page"], 1)
                self.assertTrue(data["pagination"]["has_more"])
                next_cursor = data["pagination"]["next_cursor"]
                self.assertIsNotNone(next_cursor)

            # 3. Paginated collection with cursor
            req = urllib.request.Request(f"http://127.0.0.1:5123/api/transactions?cursor={next_cursor}&limit=10")
            with urllib.request.urlopen(req) as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode())
                self.assertEqual(len(data["data"]), 10)
                self.assertEqual(data["pagination"]["offset"], 10)

            # 4. Item by ID
            first_id = data["data"][0]["id"]
            req = urllib.request.Request(f"http://127.0.0.1:5123/api/transactions/{first_id}")
            with urllib.request.urlopen(req) as resp:
                self.assertEqual(resp.status, 200)
                item_data = json.loads(resp.read().decode())
                self.assertEqual(item_data["data"]["id"], first_id)

            # 5. Simulated 429 via header
            req = urllib.request.Request("http://127.0.0.1:5123/api/transactions", headers={"X-Mock-Status": "429"})
            try:
                urllib.request.urlopen(req)
                self.fail("Expected HTTP 429")
            except urllib.error.HTTPError as e:
                self.assertEqual(e.code, 429)
                self.assertIsNotNone(e.headers.get("Retry-After"))
                err_data = json.loads(e.read().decode())
                self.assertEqual(err_data["error"], "Too Many Requests")

        finally:
            server_proc.terminate()
            server_proc.wait()
            if os.path.exists(test_file):
                os.remove(test_file)

if __name__ == "__main__":
    unittest.main()
