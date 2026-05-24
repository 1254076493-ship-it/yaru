import unittest

try:
    from app.main import app
except ModuleNotFoundError as exc:  # pragma: no cover
    app = None
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None


@unittest.skipIf(app is None, f"flask not installed: {_IMPORT_ERROR}")
class TestGenerateAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_generate_success(self):
        resp = self.client.post("/generate", json={"keywords": "护肤,熬夜"})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("content", data)
        self.assertTrue(data["content"].endswith("——XX出品"))

    def test_generate_empty_keywords(self):
        resp = self.client.post("/generate", json={"keywords": ""})
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertEqual(data["error"], "请输入关键词")


if __name__ == "__main__":
    unittest.main()
