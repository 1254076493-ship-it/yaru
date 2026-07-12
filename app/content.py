from dataclasses import dataclass

from .rules import KNOWLEDGE


@dataclass(frozen=True)
class ContentTask:
    topic: str
    audience: str
    confusion: str
    fear: str
    desired_understanding: str
    occasion: str
    opening_year: str
    goal: str
    cta_keyword: str
    product_facts: list[str]
    additional_context: str = ""


PROFILES = {
    "letter": ("家书", "多年后只剩一坛酒，却没有父母当时想说的话", "先写当下真实发生的事，再写祝福", "家书不是附赠品，而是让孩子在未来听见父母此刻声音的时间证据。"),
    "imprint": ("手脚印", "坛子好看，却看不出为什么属于这个孩子", "把孩子当时独有的身体印记留下", "小小的掌纹和足印会长大，但封坛那天的尺寸不会再回来。"),
    "generations": ("三代共封", "人都到了，祝福却混成一句热闹话", "让每一代人分别留下自己的位置", "外公外婆写源起，爷爷奶奶写护佑，父母写陪伴，三代关系才真正进入这坛酒。"),
    "inspection": ("定期检查", "封完多年不管，直到跑酒才发现", "把检查变成长期保存的一部分", "长期保存不是封口完成就结束，而是每年看一眼封口、液位和环境。"),
    "quantity": ("封几坛", "数量凭热闹决定，未来却不知道怎么开", "先安排开启节点，再决定坛数", "一坛可以留给成人礼，三坛可以分别对应冠礼、金榜题名和婚礼。"),
    "makeup": ("补封", "因为错过满月或周岁，干脆什么都不留", "把重点从错过的日期移回未来开启", "纪念的价值不只来自准时，更来自一家人今天愿意认真开始。"),
    "brand": ("品牌选择", "把品牌名当成长期保存的全部保证", "先看酒体、封口、环境和专属信息", "品牌解决识别度，却不能替代这坛酒是否适合久放、是否真正属于孩子。"),
    "packaging": ("包装判断", "第一眼很体面，长期保存需要的部分却没有问", "把包装放到酒体和封口之后判断", "礼盒负责当下好看，酒体和封口才承担多年后的结果。"),
    "timing": ("封坛时点", "为了赶节点仓促选择，反而留下长期隐患", "先确定用途和开启时间，再安排封坛", "满月、百天和周岁都可以成为起点，真正影响选择的是准备存多久、以后怎么开。"),
    "storage": ("长期保存", "多年后酒体、封口或环境经不起时间", "先把酒体、封口、环境三件事问清", "想放二十年，不能只问今天好不好看，还要问每一年怎样被照看。"),
}


def _profile(topic: str):
    checks = [
        ("letter", ("家书", "寄语")), ("imprint", ("手脚印", "手印", "脚印")),
        ("generations", ("三代", "爷爷", "奶奶", "外公", "外婆")),
        ("inspection", ("检查", "陪检", "跑酒")), ("quantity", ("几坛", "数量", "三坛")),
        ("makeup", ("补封", "错过")), ("brand", ("茅台", "品牌")),
        ("packaging", ("包装", "礼盒", "体面")), ("timing", ("满月", "什么时候", "时点")),
    ]
    for key, words in checks:
        if any(word in topic for word in words): return key, PROFILES[key]
    return "storage", PROFILES["storage"]


def _titles(task: ContentTask, p: tuple[str, str, str, str]) -> list[dict[str, str]]:
    focus, risk, advice, _ = p; o, y = task.occasion, task.opening_year
    return [
        {"type":"risk","text":f"{task.topic}，最怕的是{risk}"},
        {"type":"risk","text":f"{o}封酒准备放{y}，{focus}这一步别等以后才补"},
        {"type":"risk","text":f"给孩子封坛忽略{focus}，多年后可能只剩一场空仪式"},
        {"type":"risk","text":f"认真准备封坛酒，别在{focus}上留下未来的遗憾"},
        {"type":"contrast","text":f"{focus}不是为了现在好看，是为了{y}后还能认出来"},
        {"type":"contrast","text":f"封坛酒越追求一步到位，越要先把{focus}想清楚"},
        {"type":"contrast","text":f"真正值得留下的不是形式，而是{advice}"},
        {"type":"empathy","text":f"第一次做{o}封酒，纠结{focus}并不是想太多"},
        {"type":"empathy","text":f"想把礼物留到{y}后，这份关于{focus}的担心很真实"},
        {"type":"consult","text":f"{focus}到底怎么选？先把用途、年限和家庭情况说清楚"},
    ]


def _paragraphs(task: ContentTask, p: tuple[str, str, str, str]) -> list[tuple[str, str]]:
    focus, risk, advice, insight = p
    facts = "、".join(task.product_facts) if task.product_facts else "没有提供具体产品参数"
    return [
        ("🧭 先把真正的担心说出来", f"{task.audience}问“{task.topic}”时，表面纠结的是{task.confusion}，背后怕的是{task.fear}。如果不先说清这个后果，文章很容易只讲产品，没有回答父母为什么犹豫。"),
        (f"🔎 {focus}应该放在什么位置", f"这一步要解决的不是形式，而是{risk}。更稳妥的思路是：{advice}。{insight}"),
        ("🍶 再回到能不能长期留下", f"{KNOWLEDGE['seal']}{KNOWLEDGE['storage']}如果准备放{task.opening_year}，酒体、封口和保存环境要分别确认，不能用一个漂亮包装代替全部判断。"),
        ("🖐️ 让未来的人看得懂", f"{KNOWLEDGE['identity']}封坛不是替孩子决定未来喝什么，而是让他打开时知道：这份礼物为什么在这一天开始，又是谁一直替他保存。"),
        ("📋 现在可以怎样判断", f"先写下开启年份和使用场景，再核对{focus}、酒体、封口、存放位置。本次能够使用的产品事实只有：{facts}。没有提供的产区、年份和工艺不自行补写。"),
        ("🌿 把选择留回自己家", f"最后想清三句话：留的是酒还是时间？未来谁来打开？开坛那天希望谁在场、说什么？答案不同，适合的做法也会不同。本文希望讲明白的是：{task.desired_understanding}。"),
        ("⚠️ 如果这一层没有提前想", f"用户担心的“{task.fear}”不会因为仪式完成就自动消失。围绕{focus}留下可核对的信息，才能让以后检查、调整和开坛都有依据，而不是只能凭当年的印象猜测。"),
        ("✅ 一份可以带走的顺序", f"第一步写清为什么封；第二步确认准备保存{task.opening_year}；第三步核对{advice}；第四步把姓名、日期、家书和检查安排保存下来。顺序清楚，比一次塞进更多装饰更有用。"),
    ]


def _fit(blocks: list[tuple[str,str]], cta: str, low: int, high: int) -> str:
    chosen=[]
    for block in blocks:
        trial="\n\n".join(f"{a}\n{b}" for a,b in chosen+[block])+cta
        if len(trial)<=high: chosen.append(block)
    text="\n\n".join(f"{a}\n{b}" for a,b in chosen)+cta
    additions=[
        "这不是追求复杂，而是把多年后的风险提前问清。",
        "现在多问一句，未来就少一层说不清的遗憾。",
        "具体方案仍要结合预算、酒体和家庭计划判断。",
        "一坛一故事，先要让故事里的信息真实、具体、可辨认。",
    ]
    for sentence in additions:
        if len(text)<low and len(text)+len(sentence)+2<=high: text=text.removesuffix(cta)+"\n\n"+sentence+cta
    return text


def generate_content(task: ContentTask) -> dict:
    key,p=_profile(task.topic); titles=_titles(task,p); blocks=_paragraphs(task,p)
    cta=f"\n\n想继续核对自家的情况，可以留言“{task.cta_keyword}”，先拿一份判断清单。"
    short=_fit(blocks[:4],cta,480,520)
    long_blocks=blocks + ([("📝 这次创作补充",task.additional_context)] if task.additional_context else [])
    long=_fit(long_blocks,cta,850,930)
    return {"platform":"xiaohongshu","generator":"rules-prototype","topic_profile":key,"titles":titles,"recommended_title":titles[0]["text"],"short_content":short,"long_content":long,"warnings":[] if task.product_facts else ["未提供产品事实，内容只使用通用知识，不生成具体产品承诺。"]}
