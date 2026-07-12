import unittest
from app.content import ContentTask,generate_content
from app.validator import validate_result

class RulesTest(unittest.TestCase):
    def setUp(self): self.task=ContentTask("周岁封酒","新手父母","不知道先看什么","酒放坏","先看酒体封口储存","周岁","20年","收藏","周岁",["53度酱香酒"])
    def test_title_mix(self):
        r=generate_content(self.task); types=[x['type'] for x in r['titles']]; self.assertEqual(types.count('risk'),4); self.assertEqual(types.count('contrast'),3); self.assertEqual(types.count('empathy'),2); self.assertEqual(types.count('consult'),1)
    def test_banned_words(self):
        r=generate_content(self.task); joined=str(r); self.assertNotIn('私信',joined); self.assertNotIn('XX出品',joined)
    def test_validation_has_real_metrics(self):
        r=generate_content(self.task); check=validate_result(r,'周岁'); self.assertEqual(check['metrics']['title_count'],10); self.assertGreater(check['metrics']['short_length'],0)

if __name__=='__main__': unittest.main()
