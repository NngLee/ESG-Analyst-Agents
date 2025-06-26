from openai import OpenAI
import os
from dotenv import load_dotenv

# 加载 .env 文件中的 API 密钥（推荐）
load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def query_deepseek_esg_score(disclosure_text, dimension="environment"):
    """
    用 DeepSeek GPT（通过 OpenAI SDK）分析 ESG 维度得分
    """
    prompt = f"""
你是一位专业的 ESG 分析师。请根据以下企业披露内容，从“{dimension}”维度打分，分数为 0~1 之间的一个浮点数，仅返回该数值即可：

企业披露如下：
{disclosure_text}
    """.strip()

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位专业的 ESG 分析师"},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )
        return float(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"[DeepSeek API Error] {e}")
        return 0.5