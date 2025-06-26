import random
from deepseek_api import query_deepseek_esg_score

class FirmAgent:
    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        self.model = model
        self.investment_received = 0

    def step(self):
        disclosure = {
            'env': random.uniform(0.3, 0.7),
            'soc': random.uniform(0.3, 0.7),
            'gov': random.uniform(0.3, 0.7)
        }
        self.model.submit_disclosure(self, disclosure)

class InvestorAgent:
    def __init__(self, unique_id, model, alpha=0.7, beta=0.3):
        self.unique_id = unique_id
        self.model = model
        self.alpha = alpha
        self.beta = beta

    def step(self):
        firm_scores = self.model.get_firm_scores()
        total_weight = sum(
            self.alpha * f['return'] + self.beta * f['esg_score']
            for f in firm_scores.values()
        )
        for firm, score in firm_scores.items():
            weight = (self.alpha * score['return'] + self.beta * score['esg_score']) / total_weight
            firm.investment_received += weight * 100

class ESGAnalystAgent:
    def __init__(self, unique_id, model, dimension):
        self.unique_id = unique_id
        self.model = model
        self.dimension = dimension

    def step(self):
        disclosures = self.model.current_disclosures
        for firm, disclosure in disclosures.items():
            esg_text = self.format_disclosure(disclosure)
            score = query_deepseek_esg_score(esg_text, self.dimension)
            self.model.assign_score(firm, self.dimension, score)

    def format_disclosure(self, disclosure_dict):
        return (
            f"环境信息: {disclosure_dict['env']:.2f}; "
            f"社会信息: {disclosure_dict['soc']:.2f}; "
            f"治理信息: {disclosure_dict['gov']:.2f}"
        )