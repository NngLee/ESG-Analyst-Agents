from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
def query_esg_score(text: str, dimension: str = "environment") -> float:
    prompt = f"""
你是一个中国上市公司ESG分析专家。现在请你根据企业的披露内容，从“{dimension}”维度进行评分，参考评分标准如下：

1. ESG评分从 0 到 100 分，100 分为该维度最佳实践水平。
2. 请参考企业在该维度的“主动管理水平”与“风险暴露程度”：
   - 主动管理指标包括：管理制度、披露透明度、目标设定、执行成效等。
   - 风险暴露指标包括：已发生或潜在ESG风险事件的严重程度。
3. 请只返回一个浮点数，代表该企业在该维度的最终评分（保留两位小数）。

企业披露内容如下：
{text}
    """.strip()

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位专业的ESG评分专家。"},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )
        score = float(response.choices[0].message.content.strip())
        return max(0.0, min(100.0, score))
    except Exception as e:
        print(f"[DeepSeek ESG评分接口出错]：{e}")
        return 50.0

def generate_esg_commentary(disclosure_text: str, scores: dict) -> str:
    prompt = f"""
你是一位专业的 ESG 投资顾问，请根据以下企业的 ESG 披露内容，以及其评分结果，对该企业进行如下输出：

1. ESG 总结性评价（200 字以内）：简要说明该企业在环境、社会、治理方面的亮点与问题；
2. 投资建议（简洁明确）：是否建议在 ESG 维度上积极投资该企业，以及需注意的风险点。

企业 ESG 披露如下：
{disclosure_text}

ESG 评分如下：
环境得分：{scores.get("env", 0):.2f}
社会得分：{scores.get("soc", 0):.2f}
治理得分：{scores.get("gov", 0):.2f}
综合得分：{scores.get("esg_score", 0):.2f}，评级等级：{scores.get("esg_rating", "无")}

请按以下格式输出：
---
【ESG评价】：……
【投资建议】：……
---
    """.strip()

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个负责任的 ESG 投资顾问"},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ESG评估总结生成失败]：{e}")
        return "【ESG评价】：暂无评估。\n【投资建议】：建议谨慎评估后再做决策。"
