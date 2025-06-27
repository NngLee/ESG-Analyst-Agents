from agents import EnvironmentAgent, SocialAgent, GovernanceAgent, FirmAgent, InvestorAgent
from utils import map_score_to_rating

class ESGModel:
    def __init__(self, firms_data=None, N_firms=3, N_investors=2):
        """
        初始化ESG模型，可传入firms_data列表以指定分析的公司。
        如果未提供firms_data，则默认创建 N_firms 个虚拟公司进行模拟。
        """
        self.firms = []
        if firms_data:
            # 根据提供的数据创建对应的 FirmAgent 实例
            for i, fdata in enumerate(firms_data):
                firm = FirmAgent(unique_id=fdata.get("id", i), model=self,
                                 firm_name=fdata.get("name"),
                                 ticker=fdata.get("ticker"),
                                 cik=fdata.get("cik"),
                                 city=fdata.get("city"),
                                 country_code=fdata.get("country"))
                self.firms.append(firm)
        else:
            # 未提供特定公司时，创建虚拟公司
            self.firms = [FirmAgent(i, self) for i in range(N_firms)]

        # 创建投资者Agent列表
        self.investors = [InvestorAgent(100 + i, self) for i in range(N_investors)]
        # 创建单例的环境、社会、治理评分Agent
        self.env_agent = EnvironmentAgent(self)
        self.soc_agent = SocialAgent(self)
        self.gov_agent = GovernanceAgent(self)
        # 字典用于暂存企业披露内容和评分结果
        self.current_disclosures = {}
        self.scores = {}

    def submit_disclosure(self, firm, disclosure: str):
        """由FirmAgent调用，将企业披露内容提交给模型暂存。"""
        self.current_disclosures[firm] = disclosure

    def assign_score(self, firm, dimension: str, score: float):
        """由ESG评分Agent调用，记录某企业某维度的得分。"""
        if firm not in self.scores:
            self.scores[firm] = {}
        self.scores[firm][dimension] = score

    def get_firm_scores(self) -> dict:
        """
        汇总每个企业的ESG得分，计算综合分和评级，返回结果字典。
        """
        result = {}
        for firm in self.firms:
            # 获取各维度得分，没有则按0计
            sc = self.scores.get(firm, {})
            env_score = sc.get("env", 0.0)
            soc_score = sc.get("soc", 0.0)
            gov_score = sc.get("gov", 0.0)
            # 计算综合ESG分（加权平均，可根据需要调整权重）
            total = 0.33 * env_score + 0.33 * soc_score + 0.34 * gov_score
            rating = map_score_to_rating(total)
            result[firm] = {
                "env": env_score,
                "soc": soc_score,
                "gov": gov_score,
                "esg_score": total,
                "esg_rating": rating,
                "investment_return": 1.0 + firm.investment_received / 1000.0  # 简单收益模拟
            }
        return result

    def step(self):
        """运行模型一次迭代：收集披露、计算评分、执行投资决策。"""
        # 重置上一轮数据
        self.current_disclosures.clear()
        self.scores.clear()
        # 1. 获取每个企业的披露内容
        for firm in self.firms:
            firm.investment_received = 0  # 重置投资金额
            firm.step()  # 会调用submit_disclosure提交披露文本
        # 2. 由各ESG维度Agent对披露打分
        self.env_agent.step()
        self.soc_agent.step()
        self.gov_agent.step()
        # 3. 投资者Agent根据评分决策投资
        for investor in self.investors:
            investor.step()