import unittest

from app.generator import generate_copy


class TestGeneratorRules(unittest.TestCase):
    def test_signature_is_appended(self):
        text = generate_copy("护肤,熬夜")
        self.assertTrue(text.endswith("——XX出品"))

    def test_length_rule_on_body(self):
        text = generate_copy("护肤,熬夜,补水")
        body = text.removesuffix("——XX出品")
        self.assertGreaterEqual(len(body), 80)
        self.assertLessEqual(len(body), 150)

    def test_structure_rule(self):
        text = generate_copy("健身")
        self.assertIn("先别急着划走", text)
        self.assertIn("我按实用场景来写", text)
        self.assertIn("如果你也想要同款风格", text)


if __name__ == "__main__":
    unittest.main()
