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

def _titles(task: ContentTask) -> list[dict[str, str]]:
    y, o = task.opening_year or "多年", task.occasion
    return [
        {"type":"risk","text":f"{o}封酒想放{y}，最怕的不是不好看，是以后留不住"},
        {"type":"risk","text":f"给孩子封酒准备放{y}，这3个坑最好提前看清"},
        {"type":"risk","text":f"{o}封酒别急着看包装，放久以后出问题的常在里面"},
        {"type":"risk","text":"封酒多年后才发现选错，认真准备的父母最怕这种遗憾"},
        {"type":"contrast","text":f"给孩子留酒不难，难的是{y}后他还能认出这是留给他的"},
        {"type":"contrast","text":f"越追求{o}封酒的体面，越容易忽略长期保存"},
        {"type":"contrast","text":"真正值得留下的封坛酒，不只是一坛酒"},
        {"type":"empathy","text":f"第一次给孩子做{o}封酒，我也怕多年后只剩一个空仪式"},
        {"type":"empathy","text":"想给孩子留份长期礼物，这些担心并不是想太多"},
        {"type":"consult","text":f"{o}封酒该先问什么？把用途、年限和预算说清楚"},
    ]

def _sections(task: ContentTask, compact: bool) -> list[tuple[str,str]]:
    facts = "；".join(task.product_facts) if task.product_facts else "本次没有提供可核验的产品参数"
    storage = KNOWLEDGE["seal"] + KNOWLEDGE["storage"]
    if not compact: storage = KNOWLEDGE["degree"] + storage
    return [
      ("🧭 先看清这次要留什么",f"{task.audience}常卡在：{task.confusion}。真正需要先回答的，是这坛酒准备在{task.opening_year}后由谁打开、在什么场合打开。用途不清楚，后面的选择就容易被包装和品牌带着走。"),
      ("🍶 再看酒能不能稳稳放住",f"{storage}本次可使用的事实只有：{facts}。没有提供的年份、产区和工艺，不应该为了文案好看自行补上。"),
      ("🖐️ 最后留下孩子能认出的部分",f"{KNOWLEDGE['identity']}给孩子封坛，不只是把一个东西存起来，而是把家庭此刻的样子留给未来。"),
      ("📌 做决定前问自己三句话",f"留的是酒，还是一段时间？未来谁来喝？开坛那天，希望谁在场、说什么？想清楚这三句，才更接近“{task.desired_understanding}”。"),
    ]

def _render(task: ContentTask, compact: bool) -> str:
    body = "\n\n".join(f"{a}\n{b}" for a,b in _sections(task, compact))
    cta = f"\n\n想继续核对自家的情况，可以留言“{task.cta_keyword}”，先拿一份判断清单。"
    target = 500 if compact else 880
    if task.additional_context and not compact: body += f"\n\n📝 这次创作补充\n{task.additional_context}"
    filler = "具体选择还要回到酒体、封口、存放环境和家庭使用场景，不能只凭一个包装下结论。"
    while len(body+cta) < target-len(filler): body += f"\n\n{filler}"
    return body+cta

def generate_content(task: ContentTask) -> dict:
    titles = _titles(task)
    return {"platform":"xiaohongshu","generator":"rules-prototype","titles":titles,"recommended_title":titles[0]["text"],"short_content":_render(task,True),"long_content":_render(task,False),"warnings":[] if task.product_facts else ["未提供产品事实，内容只使用通用知识，不生成具体产品承诺。"]}
