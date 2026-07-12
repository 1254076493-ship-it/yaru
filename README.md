# 天才的酒｜小红书内容生产工作台

这是第一阶段规则引擎原型，不冒充真实 AI。它把真实创作任务结构化，输出 10 个分类标题、短文、长文和硬规则验收报告。

当前只支持小红书，先验证“生成—验收—返工”闭环，再扩展抖音、视频号和公众号。

## 运行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

访问 `http://127.0.0.1:5000`。

## 测试

```bash
python -m unittest discover -s tests -v
```

核心 API 测试不得跳过。GitHub Actions 会在 push 和 pull request 时运行同一组测试。

## 当前边界

- 生成结果来自可审计的规则原型，不是模型生成。
- 未提供的年份、产区、工艺和产品事实不会被自动补写。
- 当前验收覆盖标题配比、禁用词、CTA、字数和基础排版；传播力、AI 味和事实语境仍需进入下一阶段的模型评审。
