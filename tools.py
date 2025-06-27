# tools.py
import requests
import wikipedia
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries

# ——— 1. Yahoo Finance ———
def yahoo_finance(ticker: str) -> str:
    tk = yf.Ticker(ticker.upper())
    price = tk.info.get("regularMarketPrice", "N/A")
    pe    = tk.info.get("trailingPE", "N/A")
    return f"{ticker} 现价：{price}；PE(TTM)：{pe}"

# ——— 2. Alpha Vantage ———
ALPHA_KEY = "E0IPPXV9QP4PJSHF"
ts = TimeSeries(key=ALPHA_KEY, output_format="json")
def alpha_vantage_price(ticker: str) -> str:
    try:
        data, _ = ts.get_daily(symbol=ticker.upper(), outputsize="compact")
        latest = sorted(data.keys(), reverse=True)[0]
        close = data[latest]["4. close"]
        return f"{ticker} {latest} 收盘价：{close}"
    except Exception as e:
        return f"Alpha Vantage 调用失败（可能是无效代码）：{ticker}"


# ——— 3. OpenAQ ———
def openaq_pm25(city: str) -> str:
    resp = requests.get(
        "https://api.openaq.org/v2/latest",
        params={"city": city, "parameter": "pm25", "limit": 1}
    ).json()
    m = resp.get("results", [])
    if not m: return f"未获取到 {city} 空气质量"
    val = m[0]["measurements"][0]["value"]
    return f"{city} PM2.5：{val} µg/m³"

# ——— 4. Wikipedia ———
def wiki_summary(term: str) -> str:
    try:
        wikipedia.set_lang("zh")
        return wikipedia.summary(term, sentences=2)
    except Exception:
        return f"Wikipedia 无法找到“{term}”"

# ——— 5. SEC EDGAR ———
def sec_edgar_10k(cik: str) -> str:
    url = f"https://data.sec.gov/api/xbrl/companyfacts/{cik}.json"
    resp = requests.get(url, headers={"User-Agent":"chang@example.com"}).json()
    facts = resp.get("facts", {})
    try:
        board = facts["dei"]["BoardOfDirectorsMemberCount"]["units"]["numeric"][0]["value"]
        return f"董事会成员数：{board}"
    except:
        return "无法获取董事会成员数"

# ——— 6. World Bank ———
def world_bank_indicator(country: str, indicator: str) -> str:
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
    resp = requests.get(url, params={"format":"json","per_page":5}).json()
    data = resp[1] if len(resp)>1 else []
    entries = [f"{e['date']}:{e['value']}" for e in data if e["value"] is not None]
    return f"{country} {indicator}：{'；'.join(entries)}"
