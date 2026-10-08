import os
import datetime
import google.generativeai as genai

# 1. 初始化配置与 API
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. 动态计算学习进度与话题
START_DATE = datetime.date(2026, 10, 6) # 设置你的学习起始日
today = datetime.date.today()
day_count = (today - START_DATE).days + 1

# 难度与话题轮换逻辑
difficulty = "A2" if day_count <= 60 else "B1" # 前60天A2，之后B1
topics = ["日常生活", "文史", "哲学", "经济", "社会学"]
current_topic = topics[day_count % len(topics)]

# 3. 核心提示词（Prompt）设计
prompt = f"""
你现在是一位专业的歌德学院德语教师，精通《交际德语》、《走遍德国》、《柏林德语》和《Menschen》的教学大纲。
请为我生成第 {day_count} 天的学习内容。
当前目标语言水平：{difficulty}。
今天的主题领域：{current_topic}。

请严格按照以下 HTML 格式输出，不要包含任何 markdown 标记，直接输出 HTML 代码：

<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Day {day_count} - {difficulty} 德语每日学习</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; padding: 15px; color: #333; background-color: #f9f9f9; }}
        h1 {{ font-size: 1.5rem; color: #004d40; border-bottom: 2px solid #004d40; padding-bottom: 5px; }}
        h2 {{ font-size: 1.2rem; color: #00796b; margin-top: 20px; }}
        .word-card {{ background: #fff; padding: 10px; margin-bottom: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .word-title {{ font-weight: bold; font-size: 1.1rem; color: #d32f2f; }}
        .article-box {{ background: #e0f2f1; padding: 15px; border-radius: 8px; }}
        .grammar-box {{ background: #fff3e0; padding: 15px; border-radius: 8px; margin-top: 10px; }}
        .writing-box {{ background: #e8eaf6; padding: 15px; border-radius: 8px; margin-top: 10px; }}
    </style>
</head>
<body>
    <h1>Day {day_count} | 级别: {difficulty} | 主题: {current_topic}</h1>

    <h2>第一部分：每日 25 词核心词汇</h2>
    <!-- 请在这里生成25个单词。要求：
         1. 名词必须包含冠词和复数 (如: der Tisch, -e)。
         2. 动词必须包含第三人称单数、过去式、过去分词 (如: gehen, geht, ging, ist gegangen)。
         3. 每个单词提供1个常见搭配和1个A2-B1难度的完整例句和中文翻译。
         使用 <div class="word-card"> 包含每个单词。-->

    <h2>第二部分：主题阅读与语法解析</h2>
    <!-- 请在这里生成一篇约 150-200 词的文章，紧扣 {current_topic}。
         使用 <div class="article-box"> 包含德文原文与中文精译。
         使用 <div class="grammar-box"> 提炼文章中出现的 2-3 个核心语法点和关键句型进行重点讲解。-->

    <h2>第三部分：写作训练</h2>
    <!-- 请基于今天的主题和词汇，布置一个写作任务。
         使用 <div class="writing-box"> 提供任务要求，并提供一篇 50-100 词的满分范文及解析。-->
</body>
</html>
"""

# 4. 调用 API 并生成文件
response = model.generate_content(prompt)
html_content = response.text.replace("```html", "").replace("```", "").strip()

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print("今日内容生成完毕！")
