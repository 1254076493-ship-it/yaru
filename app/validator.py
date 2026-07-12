from collections import Counter
from .rules import BANNED_PHRASES, EMPTY_PHRASES, TITLE_GROUPS

def _issue(code, level, message, evidence=""):
    return {"code":code,"level":level,"message":message,"evidence":evidence}

def validate_result(result: dict, cta_keyword: str) -> dict:
    issues=[]; titles=result.get("titles",[]); counts=Counter(x.get("type") for x in titles)
    if len(titles)!=10 or any(counts[k]!=v for k,v in TITLE_GROUPS.items()): issues.append(_issue("title_mix","fail","标题必须为风险4、反差3、共鸣2、咨询1。"))
    texts=[result.get("short_content",""),result.get("long_content","")]
    joined="\n".join(texts+[x.get("text","") for x in titles])
    for phrase in BANNED_PHRASES:
        if phrase in joined: issues.append(_issue("banned_phrase","fail","出现禁用表达。",phrase))
    for phrase in EMPTY_PHRASES:
        if phrase in joined: issues.append(_issue("empty_phrase","warning","出现可能空泛的AI表达。",phrase))
    if f'留言“{cta_keyword}”' not in joined: issues.append(_issue("cta","fail","没有使用指定留言关键词。",cta_keyword))
    sl,ll=map(len,texts)
    if not 480<=sl<=520: issues.append(_issue("short_length","fail","短文应为480—520字。",str(sl)))
    if not 850<=ll<=930: issues.append(_issue("long_length","fail","长文应为850—930字。",str(ll)))
    for name,text in zip(("短文","长文"),texts):
        if text.count("\n\n")<3 or not all(x in text for x in ("🧭","🍶","🖐️","📌")): issues.append(_issue("layout","fail",f"{name}缺少小标题、Emoji或清晰分段。"))
    failed=any(x["level"]=="fail" for x in issues)
    return {"status":"fail" if failed else ("warning" if issues else "pass"),"issues":issues,"metrics":{"title_count":len(titles),"short_length":sl,"long_length":ll}}
