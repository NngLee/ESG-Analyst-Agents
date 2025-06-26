from agents import FirmAgent, InvestorAgent, ESGAnalystAgent

class ESGModel:
    def __init__(self, N_firms=5, N_investors=3):
        self.current_disclosures = {}
        self.scores = {}

        self.firms = [FirmAgent(i, self) for i in range(N_firms)]
        self.investors = [InvestorAgent(100 + i, self) for i in range(N_investors)]
        self.analysts = [ESGAnalystAgent(200 + i, self, dim) for i, dim in enumerate(['env', 'soc', 'gov'])]

    def submit_disclosure(self, firm, disclosure):
        self.current_disclosures[firm] = disclosure

    def assign_score(self, firm, dimension, score):
        if firm not in self.scores:
            self.scores[firm] = {}
        self.scores[firm][dimension] = score

    def get_firm_scores(self):
        result = {}
        for firm in self.firms:
            firm_score = self.scores.get(firm, {'env': 0, 'soc': 0, 'gov': 0})
            composite = (
                0.33 * firm_score.get('env', 0) +
                0.33 * firm_score.get('soc', 0) +
                0.34 * firm_score.get('gov', 0)
            )
            result[firm] = {
                'esg_score': composite,
                'return': self.estimate_return(firm)
            }
        return result

    def estimate_return(self, firm):
        base = 1.0 + firm.investment_received / 1000.0
        return base

    def step(self):
        self.current_disclosures.clear()
        self.scores.clear()

        for f in self.firms:
            f.investment_received = 0
            f.step()

        for a in self.analysts:
            a.step()

        for i in self.investors:
            i.step()