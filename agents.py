from deepseek_api import query_esg_score
from tools import (
    yahoo_finance, alpha_vantage_price,
    openaq_pm25, wiki_summary,
    sec_edgar_10k, world_bank_indicator
)

class ESGDimensionAgent:
    """
    ESG维度评分通用Agent基类：根据指定维度对披露内容打分。
    """
    def __init__(self, model, dimension: str, score_key: str):
        self.model = model
        self.dimension = dimension       # 评分维度名称，例如 "environment", "society"
        self.score_key = score_key       # 在模型评分字典中的键，例如 "env", "soc", "gov"

    def step(self):
        # 遍历所有企业披露内容，调用评分接口
        for firm, disclosure in self.model.current_disclosures.items():
            try:
                score = query_esg_score(disclosure, self.dimension)
            except Exception as e:
                print(f"[警告] ESG评分接口异常（维度: {self.dimension}）：{e}")
                score = 50.0  # 出现异常时给一个中等默认分
            self.model.assign_score(firm, self.score_key, score)

class EnvironmentAgent(ESGDimensionAgent):
    """环境维度评分Agent"""
    def __init__(self, model):
        super().__init__(model, "environment", "env")

class SocialAgent(ESGDimensionAgent):
    """社会维度评分Agent"""
    def __init__(self, model):
        super().__init__(model, "society", "soc")

class GovernanceAgent(ESGDimensionAgent):
    """公司治理维度评分Agent"""
    def __init__(self, model):
        super().__init__(model, "governance", "gov")

class FirmAgent:
    """
    企业Agent：负责检索企业披露信息，并将其提交给ESG评分Agents。
    """
    def __init__(self, unique_id, model, firm_name=None, ticker=None, cik=None, city=None, country_code=None):
        self.unique_id = unique_id
        self.model = model
        # 公司名称和股票代码，如未提供股票代码则使用名称作为查询依据
        self.firm_name = firm_name or f"Firm-{unique_id}"
        self.ticker = ticker if ticker else (firm_name or f"Firm-{unique_id}")
        # 其他可选属性：CIK代码、城市、国家
        self.cik = cik
        self.city = city
        # 默认为中国，如提供了国家代码则使用提供值
        self.country_code = country_code or "CN"
        self.investment_received = 0.0
        self._cached_disclosure = None

    def fetch_base_disclosure(self) -> str:
        """
        获取企业基本披露内容。此处可替换为实际的信息检索逻辑（如读取年报摘要等）。
        """
        return f"{self.firm_name} 的最新ESG披露概况：环境管理、社会责任与公司治理情况摘要。"

    def generate_disclosure(self) -> str:
        """
        生成完整的企业披露文本，包括基本披露和来自各数据源的补充信息。
        利用缓存避免重复调用外部API。
        """
        if self._cached_disclosure:
            return self._cached_disclosure

        # 基础披露内容
        base_text = self.fetch_base_disclosure()
        extra_info = []

        # 获取财经数据（Yahoo优先，失败则尝试Alpha Vantage）
        stock_line = yahoo_finance(self.ticker)
        if not stock_line:  # 若Yahoo未获得数据，则用Alpha Vantage
            stock_line = alpha_vantage_price(self.ticker)
        if stock_line:
            extra_info.append(stock_line)

        # 空气质量数据（需要城市名）
        if self.city:
            aq_line = openaq_pm25(self.city)
            if aq_line:
                extra_info.append(aq_line)

        # 维基百科公司简介
        wiki_line = wiki_summary(self.firm_name)
        if wiki_line:
            extra_info.append(wiki_line)

        # 美国SEC年报数据（需要CIK）
        if self.cik:
            sec_line = sec_edgar_10k(self.cik)
            if sec_line:
                extra_info.append(sec_line)

        # 世界银行指标（例如人均GDP，用于提供国家背景信息，需要国家代码）
        if self.country_code:
            wb_line = world_bank_indicator(self.country_code, "NY.GDP.PCAP.CD")
            if wb_line:
                extra_info.append(wb_line)

        # 将所有部分组合成完整披露文本
        full_disclosure = base_text + ("\n" + "\n".join(extra_info) if extra_info else "")
        self._cached_disclosure = full_disclosure
        return full_disclosure

    def step(self):
        """
        企业Agent执行步骤：生成披露文本并提交给ESGModel进行评分。
        """
        disclosure = self.generate_disclosure()
        # 提交披露内容给模型（模型会转发给各ESG评分Agent）
        self.model.submit_disclosure(self, disclosure)

class InvestorAgent:
    """
    投资者Agent：根据ESG评分决定对企业的投资（模拟行为）。
    """
    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        self.model = model

    def step(self):
        # 简单投资逻辑：若企业综合ESG评分>70，则投资一定金额
        scores = self.model.get_firm_scores()
        for firm, score_dict in scores.items():
            if score_dict.get("esg_score", 0) > 70:
                # 平均分配投资额100（模拟），实际应用中可用更复杂逻辑
                firm.investment_received += 100.0 / len(self.model.firms)