import requests
import os

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") or "your-deepseek-api-key"
API_URL = "https://api.deepseek.com/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json"
}

def query_deepseek_esg_score(disclosure_text, dimension="environment"):
    prompt = f"""
你是一名专业的 ESG 分析师。请根据以下企业披露内容，从“{dimension}”维度给出评分（范围 0~1），仅返回一个浮点数：
{disclosure_text}
    """.strip()

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一名专业的 ESG 分析师。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"].strip()
        return float(reply)
    except Exception as e:
        print(f"[DeepSeek API Error] {e}")
        return 0.5