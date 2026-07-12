import unittest
from app.main import create_app

VALID={"topic":"周岁封酒想存20年","audience":"第一次给孩子封酒的新手父母","confusion":"先看品牌还是酒体","fear":"多年后不能喝","desired_understanding":"先看酒体、封口和储存","occasion":"周岁","opening_year":"20年","goal":"收藏","cta_keyword":"周岁","product_facts":["53度酱香酒","素烧陶坛"]}

class ApiTest(unittest.TestCase):
    def setUp(self): self.client=create_app(testing=True).test_client()
    def test_generate(self):
        r=self.client.post('/generate',json=VALID); self.assertEqual(r.status_code,200); data=r.get_json(); self.assertEqual(len(data['titles']),10); self.assertIn('self_check',data)
    def test_missing_fields_fail_instead_of_skip(self):
        r=self.client.post('/generate',json={"topic":"周岁"}); self.assertEqual(r.status_code,400); self.assertIn('fields',r.get_json())
    def test_non_json(self): self.assertEqual(self.client.post('/generate',data='x').status_code,400)

if __name__=='__main__': unittest.main()
