import os
import requests
import certifi
import wikipedia
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries

# 设置证书路径，防止HTTPS证书错误
os.environ['SSL_CERT_FILE'] = certifi.where()

# 初始化 Alpha Vantage API
ALPHA_KEY = os.getenv("ALPHA_VANTAGE_KEY", "E0IPPXV9QP4PJSHF")  # 建议将API密钥设为环境变量
_ts = TimeSeries(key=ALPHA_KEY, output_format="json")

def yahoo_finance(ticker: str) -> str:
    """获取股票当前价格和市盈率（来自Yahoo财经）。"""
    try:
        ticker = ticker.upper()
        tk = yf.Ticker(ticker)
        info = tk.info
        price = info.get("regularMarketPrice")
        pe = info.get("trailingPE")
        if price is None or pe is None:
            # 如未能获取完整数据，则触发异常以使用后备方案
            raise ValueError("Ticker data not available")
        return f"{ticker} 当前股价：{price}；市盈率PE(TTM)：{pe}"
    except Exception as e:
        return ""  # 返回空串用于后续备用处理

def alpha_vantage_price(ticker: str) -> str:
    """获取股票最新收盘价（来自Alpha Vantage）。"""
    try:
        ticker = ticker.upper()
        data, _ = _ts.get_daily(symbol=ticker, outputsize="compact")
        latest_date = sorted(data.keys(), reverse=True)[0]
        close_price = data[latest_date]["4. close"]
        return f"{ticker} {latest_date} 收盘价：{close_price}"
    except Exception as e:
        return ""  # 获取失败返回空，后续可以选择忽略

def openaq_pm25(city: str) -> str:
    """获取指定城市的PM2.5空气质量指标（来自OpenAQ）。"""
    try:
        resp = requests.get(
            "https://api.openaq.org/v2/latest",
            params={"city": city, "parameter": "pm25", "limit": 1},
            timeout=5
        )
        if resp.status_code != 200:
            raise Exception(f"HTTP {resp.status_code}")
        data = resp.json().get("results", [])
        if not data:
            return f"{city} 空气质量数据未找到。"
        value = data[0]["measurements"][0]["value"]
        return f"{city} PM2.5：{value} µg/m³"
    except Exception as e:
        return f"{city} 空气质量获取失败。"

def wiki_summary(term: str) -> str:
    """获取维基百科词条摘要（优先中文，可备用英文）。"""
    try:
        wikipedia.set_lang("zh")
        return wikipedia.summary(term, sentences=2)
    except Exception as e:
        try:
            # 若中文维基未找到，则尝试英文维基
            wikipedia.set_lang("en")
            return wikipedia.summary(term, sentences=2)
        except Exception:
            return f"未找到“{term}”的百科信息。"

def sec_edgar_10k(cik: str) -> str:
    """获取美国SEC EDGAR公司年报信息（示例：董事会成员数）。"""
    try:
        url = f"https://data.sec.gov/api/xbrl/companyfacts/{cik}.json"
        headers = {"User-Agent": "example@domain.com"}  # 提供联系人以符合SEC要求
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            raise Exception(f"HTTP {resp.status_code}")
        facts = resp.json().get("facts", {})
        # 提取董事会成员数量
        board_count = facts["dei"]["BoardOfDirectorsMemberCount"]["units"]["numeric"][0]["value"]
        return f"董事会成员数：{board_count}"
    except Exception as e:
        return "董事会成员数信息获取失败。"

def world_bank_indicator(country_code: str, indicator: str) -> str:
    """获取世界银行指定指标数据（如人均GDP），国家代码为ISO两位代码。"""
    try:
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}"
        resp = requests.get(url, params={"format": "json", "per_page": 5}, timeout=5)
        if resp.status_code != 200:
            raise Exception(f"HTTP {resp.status_code}")
        data = resp.json()
        if len(data) < 2 or not data[1]:
            return f"{country_code} 指标{indicator}暂无数据。"
        entries = [f"{entry['date']}年: {entry['value']}" for entry in data[1] if entry.get("value") is not None]
        if not entries:
            return f"{country_code} 指标{indicator}暂无数据。"
        return f"{country_code} {indicator} 数据：" + "；".join(entries)
    except Exception as e:
        return f"{country_code} {indicator} 数据获取失败。"