from deepseek_api import query_esg_score
import requests
class EnvironmentAgent:
    def __init__(self, model):
        self.model = model

    def step(self):
        for firm, disclosure in self.model.current_disclosures.items():
            score = query_esg_score(disclosure, "environment")
            self.model.assign_score(firm, "env", score)

class SocietyAgent:
    def __init__(self, model):
        self.model = model

    def step(self):
        for firm, disclosure in self.model.current_disclosures.items():
            score = query_esg_score(disclosure, "society")
            self.model.assign_score(firm, "soc", score)

class GovernanceAgent:
    def __init__(self, model):
        self.model = model

    def step(self):
        for firm, disclosure in self.model.current_disclosures.items():
            score = query_esg_score(disclosure, "governance")
            self.model.assign_score(firm, "gov", score)

class FirmAgent:
    def __init__(self, unique_id, model, firm_name=None):
        self.unique_id = unique_id
        self.model = model
        self.firm_name = firm_name or f"Firm-{unique_id}"
        self.investment_received = 0.0
        self.cached_disclosure = None

    def fetch_esg_disclosure(self):
        """从网络检索该企业 ESG 相关公开信息（演示：Baidu 或 Bing 简略搜索）"""
        try:
            query = f"{self.firm_name} ESG 披露 site:cn"  # 中文 ESG 公告
            url = f"https://api.deepseek.com/search?q={query}"  # 可替换为真实搜索 API 或 Bing API
            # 实际部署建议用 Bing News API / 自有 ESG 报告库
            res = requests.get(url)
            if res.ok:
                # 示例中返回模拟文本（替换为真实接口内容）
                return f"{self.firm_name} 在最近的年报中披露了环境减排目标、社会责任指标与治理结构改革。"
        except Exception as e:
            print(f"[ESG信息抓取失败]：{e}")
        return None

    def generate_disclosure(self):
        if self.cached_disclosure:
            return self.cached_disclosure

        if self.firm_name:
            disclosure = self.fetch_esg_disclosure()
            if disclosure:
                self.cached_disclosure = disclosure
                return disclosure

        return f"本企业致力于减少碳排放，提升员工福利，并加强董事会独立性。"

class InvestorAgent:
    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        self.model = model

    def step(self):
        scores = self.model.get_firm_scores()
        for firm, score_dict in scores.items():
            if score_dict["esg_score"] > 70:
                firm.investment_received += 100.0 / len(self.model.firms)