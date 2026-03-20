import os
from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# 配置 Gemini API
# 在 Render 上部署时，您需要在环境变量中配置 GEMINI_API_KEY
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# 模拟数据库：包含您近期的学业成绩
grades_db = [
    {"subject": "微分学", "date": "2026-03-10", "score": 92, "maxScore": 100},
    {"subject": "物理", "date": "2026-03-15", "score": 76, "maxScore": 100},
    {"subject": "英语口语与词汇", "date": "2026-03-12", "score": 85, "maxScore": 100}
]

@app.route("/", methods=["GET", "POST"])
def index():
    analysis_result = "请点击下方按钮获取最新的 Gemini 成绩分析。"
    
    if request.method == "POST":
        if not api_key:
            analysis_result = "错误：未检测到 Gemini API 密钥。请确保在 Render 环境中正确配置了 GEMINI_API_KEY。"
        else:
            try:
                # 构建发送给 Gemini 的提示词
                prompt = f"作为一名学术顾问，请分析以下高阶课程成绩，并给出专业的学术建议。重点分析理科逻辑与英语表达能力的发展方向：\n{grades_db}"
                
                # 调用 Gemini 模型 (使用标准文本模型)
                model = genai.GenerativeModel('gemini-1.5-pro')
                response = model.generate_content(prompt)
                analysis_result = response.text
            except Exception as e:
                analysis_result = f"调用 API 时发生错误：{str(e)}"

    return render_template("index.html", grades=grades_db, analysis=analysis_result)

if __name__ == "__main__":
    app.run(debug=True)
