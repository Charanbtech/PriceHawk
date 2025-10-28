# backend/tests/test_health.py
import unittest
from app import create_app

class HealthTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_health(self):
        rv = self.app.get("/health")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b"ok", rv.data)

if __name__ == "__main__":
    unittest.main()
