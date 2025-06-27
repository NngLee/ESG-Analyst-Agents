import sys
import argparse
from model import ESGModel
from deepseek_api import generate_esg_commentary

def resolve_company(term: str):
    """
    根据用户输入的名称或代码，推断股票代码和公司正式名称。
    返回元组 (name, ticker, city, country, cik)。
    """
    term = term.strip()
    # 简单判断输入类型
    is_ticker = term.isupper() and 1 <= len(term) <= 5  # 全大写且长度较短，视为股票代码
    if is_ticker:
        ticker = term
        # 尝试通过Yahoo财经获取公司全称
        try:
            tk = __import__('yfinance').Ticker(ticker)
            info = tk.info
            name = info.get("longName") or term
            country = info.get("country")
            city = info.get("city")
        except Exception:
            name = term
            country = None
            city = None
    else:
        name = term
        # 利用Yahoo财经搜索API查找股票代码
        try:
            import requests
            resp = requests.get("https://query2.finance.yahoo.com/v1/finance/search", params={"q": term}, timeout=5)
            data = resp.json()
            # 提取第一个搜索结果的股票代码和名称
            quotes = data.get("quotes")
            if quotes:
                ticker = quotes[0].get("symbol")
                # 如果搜索结果有正式名称，使用它
                if quotes[0].get("shortname"):
                    name = quotes[0]["shortname"]
                elif quotes[0].get("longname"):
                    name = quotes[0]["longname"]
            else:
                ticker = term  # 未找到则直接用名称当作ticker尝试
        except Exception:
            ticker = term
        country = None
        city = None
    # 返回解析结果
    return name, ticker, city, country, None  # 由于CIK难以直接获取，这里返回None

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="ESG 多智能体分析系统")
    parser.add_argument("company", help="公司名称或股票代码")
    parser.add_argument("--city", help="公司所在城市（用于环境数据）", default=None)
    parser.add_argument("--country", help="公司所在国家的ISO代码（用于国家指标）", default=None)
    parser.add_argument("--cik", help="公司在SEC的CIK代码（用于美国年报数据）", default=None)
    args = parser.parse_args()

    # 解析输入参数
    user_input = args.company
    # 通过辅助函数解析名称和代码
    name, ticker, city, country, cik = resolve_company(user_input)
    # 如果用户有显式提供city/country/cik参数则覆盖自动推断结果
    if args.city: city = args.city
    if args.country: country = args.country
    if args.cik: cik = args.cik

    # 构造公司数据字典并创建模型
    firm_data = {
        "id": 0,
        "name": name,
        "ticker": ticker,
        "city": city,
        "country": country,
        "cik": cik
    }
    model = ESGModel(firms_data=[firm_data], N_investors=1)
    model.step()  # 执行模型分析流程

    # 获取结果并生成ESG评价与投资建议
    results = model.get_firm_scores()
    firm = model.firms[0]
    scores = results.get(firm, {})
    disclosure = model.current_disclosures.get(firm, "（暂无披露）")
    commentary = generate_esg_commentary(disclosure, scores)

    # 打印输出结果
    comp_identifier = f"{name} ({ticker})" if ticker and name and ticker != name else (name or ticker)
    print(f"\n分析对象：{comp_identifier}")
    print(f"环境得分: {scores.get('env', 0):.2f}")
    print(f"社会得分: {scores.get('soc', 0):.2f}")
    print(f"治理得分: {scores.get('gov', 0):.2f}")
    print(f"综合ESG得分: {scores.get('esg_score', 0):.2f}，评级: {scores.get('esg_rating', 'N/A')}")
    print("ESG综合评价与投资建议：")
    print(commentary if commentary else "无")
    
if __name__ == "__main__":
    main()
