from flask import Flask, jsonify, render_template, request
from .content import ContentTask, generate_content
from .rules import ALLOWED_GOALS, ALLOWED_OCCASIONS
from .validator import validate_result

def create_app(testing=False):
    app=Flask(__name__,template_folder="../templates",static_folder="../static"); app.config["TESTING"]=testing
    @app.get("/")
    def index(): return render_template("index.html")
    @app.post("/generate")
    def generate():
        data=request.get_json(silent=True)
        if not isinstance(data,dict): return jsonify({"error":"请求必须是JSON对象"}),400
        required=("topic","audience","confusion","fear","desired_understanding","occasion","opening_year","goal","cta_keyword")
        missing=[k for k in required if not str(data.get(k,"")).strip()]
        if missing: return jsonify({"error":"缺少必填字段","fields":missing}),400
        if data["occasion"] not in ALLOWED_OCCASIONS or data["goal"] not in ALLOWED_GOALS: return jsonify({"error":"节点或内容目标不在允许范围内"}),400
        task=ContentTask(topic=str(data["topic"]).strip()[:120],audience=str(data["audience"]).strip()[:120],confusion=str(data["confusion"]).strip()[:240],fear=str(data["fear"]).strip()[:240],desired_understanding=str(data["desired_understanding"]).strip()[:240],occasion=data["occasion"],opening_year=str(data["opening_year"]).strip()[:40],goal=data["goal"],cta_keyword=str(data["cta_keyword"]).strip()[:20],product_facts=[str(x).strip()[:120] for x in data.get("product_facts",[]) if str(x).strip()][:12],additional_context=str(data.get("additional_context","")).strip()[:2000])
        result=generate_content(task); result["self_check"]=validate_result(result,task.cta_keyword)
        return jsonify(result)
    return app

app=create_app()
if __name__=="__main__": app.run(host="127.0.0.1",port=5000,debug=False)
