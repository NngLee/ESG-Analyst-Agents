from agents import EnvironmentAgent, SocietyAgent, GovernanceAgent, FirmAgent, InvestorAgent
from utils import map_score_to_rating
class ESGModel:
    def __init__(self, N_firms=3, N_investors=2):
        self.firms = [FirmAgent(i, self) for i in range(N_firms)]
        self.investors = [InvestorAgent(100 + i, self) for i in range(N_investors)]
        self.env_agent = EnvironmentAgent(self)
        self.soc_agent = SocietyAgent(self)
        self.gov_agent = GovernanceAgent(self)
        self.current_disclosures = {}
        self.scores = {}

    def submit_disclosure(self, firm, disclosure):
        self.current_disclosures[firm] = disclosure

    def assign_score(self, firm, dimension, score):
        if firm not in self.scores:
            self.scores[firm] = {}
        self.scores[firm][dimension] = score

    def get_firm_scores(self):
        result = {}
        for firm in self.firms:
            sc = self.scores.get(firm, {'env': 0, 'soc': 0, 'gov': 0})
            total = 0.33 * sc.get("env", 0) + 0.33 * sc.get("soc", 0) + 0.34 * sc.get("gov", 0)
            rating = map_score_to_rating(total)
            result[firm] = {
                "env": sc.get("env", 0),
                "soc": sc.get("soc", 0),
                "gov": sc.get("gov", 0),
                "esg_score": total,
                "esg_rating": rating,
                "return": 1.0 + firm.investment_received / 1000.0
            }
        return result

    def step(self):
        self.current_disclosures.clear()
        self.scores.clear()
        for f in self.firms:
            f.investment_received = 0
            f.step()
        self.env_agent.step()
        self.soc_agent.step()
        self.gov_agent.step()
        for i in self.investors:
            i.step()
