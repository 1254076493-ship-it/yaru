import re


def _clean_keywords(text: str) -> list[str]:
    parts = re.split(r"[，,、\s]+", text.strip())
    return [p for p in parts if p]


def generate_copy(keywords: str, signature: str = "XX") -> str:
    """
    生成 80-150 字文案，结构：开头抓眼球 + 核心卖点 + 结尾引导 + 固定落款。
    规则：口语化、短句、不夸张不虚假。
    """
    kw_list = _clean_keywords(keywords)
    topic = "、".join(kw_list[:3]) if kw_list else "这个内容"

    opening = f"先别急着划走，{topic}这事真跟你我日常有关。"
    core = (
        "我按实用场景来写，先讲你最关心的点，再把方法拆成小步骤。"
        "话不绕弯，能直接拿去用，省时间也省心。"
    )
    ending = "如果你也想要同款风格，发我关键词，我给你快速出一版。"

    text = opening + core + ending

    # 字数兜底：不够就补充一句，超出就裁剪（不含落款）
    if len(text) < 80:
        text += "重点都落在真实体验上，不整虚的。"
    if len(text) > 145:
        text = text[:145].rstrip("，。；、 ") + "。"

    return f"{text}——{signature}出品"
