import unittest
from difflib import SequenceMatcher

from app.content import ContentTask, generate_content
from app.validator import validate_result


CASES = [
    ("周岁封酒想存20年", "先看品牌还是酒体", "酒放坏", "先看酒体封口储存", "周岁", "20年", ["53度酱香酒"]),
    ("周岁封酒别被包装带跑", "包装好看是不是更重要", "以后只剩空包装", "先判断能否长期放", "周岁", "18年", ["素烧陶坛"]),
    ("给孩子封酒为什么放家书", "家书不知道写什么", "孩子以后认不出礼物", "家书要记录此刻", "周岁", "18年", ["父母家书", "手脚印"]),
    ("满月封酒怎么封", "什么时候做合适", "赶时间选错", "先确定用途和开启时间", "满月", "20年", ["姓名定制"]),
    ("错过周岁还能补封吗", "现在补还有没有意义", "错过节点留遗憾", "意义在未来开启", "补封", "18年", ["封坛日期"]),
    ("给孩子封几坛合适", "一坛还是三坛", "数量多但没有用途", "按未来节点安排数量", "周岁", "20年", ["三代共封"]),
    ("封坛酒需要每年检查吗", "封完是不是不用管", "跑酒或封口松动", "长期保存需要定期陪检", "周岁", "20年", ["定期陪检"]),
    ("必须用茅台给孩子封酒吗", "品牌越大是不是越稳", "为品牌溢价买单", "先看酒体和专属感", "周岁", "20年", ["53度酱香酒"]),
    ("手脚印为什么要留在坛上", "装饰有没有必要", "多年后缺少孩子印记", "让孩子认出礼物属于自己", "百天", "18年", ["手脚印", "姓名定制"]),
    ("三代共封有什么意义", "谁来封更合适", "仪式热闹但关系没留下", "让三代祝福各有位置", "周岁", "20年", ["三代共封", "父母家书"]),
]


def make(case):
    return ContentTask(case[0], "第一次给孩子封酒的新手父母", case[1], case[2], case[3], case[4], case[5], "收藏", "封坛", case[6])


class RegressionTest(unittest.TestCase):
    def test_ten_real_tasks_pass_hard_rules(self):
        for case in CASES:
            result = generate_content(make(case))
            self.assertEqual(validate_result(result, "封坛")["status"], "pass", case[0])

    def test_topics_do_not_collapse_to_one_template(self):
        results = [generate_content(make(case)) for case in CASES]
        profiles = {result["topic_profile"] for result in results}
        self.assertEqual(len(profiles), 10)
        texts = [result["long_content"] for result in results]
        similarity = [SequenceMatcher(None, texts[i], texts[j]).ratio() for i in range(len(texts)) for j in range(i)]
        self.assertLess(max(similarity), 0.90)


if __name__ == "__main__":
    unittest.main()
